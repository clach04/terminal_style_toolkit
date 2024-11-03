#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

# library for rendering Putty colornames (json) config files into templates

import json
import logging
import os
import re
import shlex
import sys


log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(level=logging.INFO)
#log.setLevel(level=logging.DEBUG)


default_mapping_if_missing = {
    'Colour0-hex': 'Colour20-hex',  # Default Foreground - default to ANSI White
    'Colour1-hex': 'Colour0-hex',  # Default Bold Foreground  -- equals to non-bold - default to Default Foreground
    "Colour2-hex": "Colour6-hex",  # Default Background - default to ANSI Black
    "Colour3-hex": "Colour2-hex",  # Default Bold Background  -- equals to non-bold - default to Default Background
    "Colour4-hex": "Colour2-hex",  # Cursor Text -- equals to default background - default to Default Background
    "Colour5-hex": 'Colour0-hex',  # Cursor Colour -- equals to default foreground - default to Default Foreground

    "Colour7-hex": "Colour6-hex",  # ANSI Black Bright
    "Colour9-hex": "Colour8-hex",  # ANSI Red Bright
    "Colour11-hex": "Colour10-hex",  # ANSI Green Bright
    "Colour13-hex": "Colour12-hex",  # ANSI Yellow Bright
    "Colour15-hex": "Colour14-hex",  # ANSI Blue Bright
    "Colour17-hex": "Colour16-hex",  # ANSI Magenta Bright
    "Colour19-hex": "Colour18-hex",  # ANSI Cyan Bright
    "Colour21-hex": "Colour20-hex",  # ANSI White Bright
}

### start copy from parse pallete tools ###

def unhex(hex_str):
    """dumb reverse of python builtin hex()
    returns integer value of string hex
    Examples:
        '0x17' returns 23
        '17' returns 23
    """
    return int(hex_str, 16)

def hex2rgb_ints(hex_str):
    """Given '#123456' return (18, 52, 86)
    """
    hex_str = hex_str.strip().replace('#', '')  # remove '#'
    hex_str = hex_str.strip().replace('0x', '')  # remove '0x'
    if len(hex_str) != len('123456'):
        raise NotImplementedError('input strings of length %d %r' % (len(hex_str), hex_str))

    return unhex(hex_str[0:2]), unhex(hex_str[2:4]), unhex(hex_str[4:6])

### end copy ###

class UglyMustache:
    """Do not use this, it is ugly and extremely limited (...but doesn't need an external lib)
      * no comment support
      * no white space support
      * no array support
      * no html support
      * no ... so much more stuff missing! ;-)
    """
    def render(self, template_str, input_dict):
        #import pdb; pdb.set_trace()
        for key in input_dict:
            log.debug('rendering %r', key)
            template_str = template_str.replace('{{%s}}' % key, str(input_dict[key]))
        return template_str

def render_template(putty_color_dict, template_filename='putty_reg.mustache'):
    """rendering Putty colornames (json) config files using Mustache template

    @putty_color_dict should contain Colour0-Colour21 entries
    which are EXPECTED to contain;
        either
        hex "Colour0-hex"
        or decimal "Colour0" a comma seperated string of decimal characters (from 0-255) (just like Windows Putty registry entries)

    @template_filename - filename of template, support variables:
        Colour0-hex - hex RGB
        Colour0-rgb-r Colour0-rgb-g Colour0-rgb-b  - decimals for each channel ONLY
        ...
        Colour21-hex - hex RGB
        Colour21-rgb-r Colour21-rgb-g Colour21-rgb-b  - decimals for each channel ONLY

    """
    if not os.path.exists(template_filename):
        template_filename = os.path.join(os.path.dirname(__file__), template_filename)
    f = open(template_filename)  # just assume this will work, correct text mode and encoding - assume utf-8
    template_str = f.read()
    f.close()

    scheme_name = putty_color_dict.get('scheme-name') or 'unnamed'  # pretty name
    putty_color_dict['scheme-name'] = scheme_name
    scheme_author = putty_color_dict.get('scheme-author') or 'unnamed'
    putty_color_dict['scheme-author'] = scheme_author
    #scheme_slug = putty_color_dict.get('scheme-slug', scheme_name.replace(' ', '_'))  # short name - TODO slugify if scheme_name used
    scheme_slug = putty_color_dict.get('scheme-slug') or scheme_name  # short name - TODO slugify if scheme_name used
    scheme_slug = scheme_slug.replace(' ', '%20')  # Putty has major issues if a real space is used, recommend using underscore instead but handle this edge case.
    putty_color_dict['scheme-slug'] = scheme_slug
    print('%s' % scheme_slug)
    template_dict = {}
    template_dict = {
        'scheme-name': scheme_name,
        'scheme-author': scheme_author,
        'scheme-slug': scheme_slug,
        'scheme-comment': putty_color_dict.get('scheme-comment', '')
    }
    for comment_number in range(1, 9 + 1):
        temp_template_key = 'scheme-comment%d' % comment_number
        template_dict[temp_template_key] = putty_color_dict.get(temp_template_key, '')

    """Old  code
    # Find all Colour0-Colour21 entries which are EXPECTED to contain a comma seperated string of decimal characters (from 0-255)
    for color_number in putty_color_dict:
        if not color_number.startswith('Col'):
            continue
        decimal_rgb = putty_color_dict[color_number]
        if ',' not in decimal_rgb:
            raise NotImplementedError('non decimal comma seperated value (could treat as hex...?)')
        r, g, b = map(int, decimal_rgb.split(','))
        color_dict[color_number] = '%d,%d,%d' % (r, g, b)  # Decimal RGB, as used by Putty
        #color_dict[color_number] = '%02x%02x%02x' % (r, g, b)  # Hex RGB
        template_dict['%s-hex' % color_number] = '%02x%02x%02x' % (r, g, b)  # Hex RGB
        template_dict['%s-rgb-r' % color_number] = r
        template_dict['%s-rgb-g' % color_number] = g
        template_dict['%s-rgb-b' % color_number] = b
    """
    # explictly look for Colour0-Colour21 entries, if hex ones are found use those to derive other fields, else use other fields
    #import pdb ; pdb.set_trace()
    for color_number in range(21 +1):
        color_string_prefix = 'Colour%d' % color_number
        # check for hex first
        hex_lookup_name = '%s-hex' % color_string_prefix
        try:
            hex_rgb = putty_color_dict[hex_lookup_name]  # example; ffffff
            log.debug('hex_lookup_name=%r , hex_rgb %r', hex_lookup_name, hex_rgb)
            if hex_rgb == '':
                copy_color = default_mapping_if_missing[hex_lookup_name]
                hex_rgb = putty_color_dict[copy_color]
                log.debug('copy_color=%r , hex_rgb %r', copy_color, hex_rgb)
                putty_color_dict[hex_lookup_name] = hex_rgb
                #raise KeyError
            template_dict[hex_lookup_name] = hex_rgb  # use as-is, no validation
            r, g, b = hex2rgb_ints(hex_rgb)
        except KeyError:
            # no hex so there MUST be rgb
            decimal_rgb = putty_color_dict[color_string_prefix]  # example; 255,255,255
            if ',' not in decimal_rgb:
                raise NotImplementedError('non decimal comma seperated value (could treat as hex...?)')
            r, g, b = map(int, decimal_rgb.split(','))
            template_dict[hex_lookup_name] = '%02x%02x%02x' % (r, g, b)  # Hex RGB
        except:
            log.error('when processing %r', hex_lookup_name)
            raise  # re-reraise
        template_dict['%s-rgb-r' % color_string_prefix] = r
        template_dict['%s-rgb-g' % color_string_prefix] = g
        template_dict['%s-rgb-b' % color_string_prefix] = b
        # comments and notes
        template_dict['%s-comment' % color_string_prefix] = putty_color_dict.get('%s-comment' % color_string_prefix, '')
        template_dict['%s-note' % color_string_prefix] = putty_color_dict.get('%s-note' % color_string_prefix, '')

    for entry in list(template_dict.keys()):
        log.debug('processing %r', entry)
        template_dict[entry.replace('-', '_')] = template_dict[entry]

    stache = UglyMustache()
    #print('%s' % UglyMustache.render(template_str, template_dict))  # classmethod
    return stache.render(template_str, template_dict)
