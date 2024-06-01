#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

# library for rendering Putty colornames config giles into templates

import json
import os
import re
import shlex
import sys


class UglyMustache:
    """Do not use this, it is ugly and extremely limited (...but doesn't need an external lib)
      * no white space support
      * no array support
      * no html support
      * no ... so much more stuff missing
    """
    def render(self, template_str, input_dict):
        for key in input_dict:
            template_str = template_str.replace('{{%s}}' % key, str(input_dict[key]))
        return template_str

def render_template(putty_color_dict, template_filename='putty_reg.mustache'):
    if not os.path.exists(template_filename):
        template_filename = os.path.join(os.path.dirname(__file__), template_filename)
    f = open(template_filename)  # just assume this will work, correct text mode and encoding - assume utf-8
    template_str = f.read()
    f.close()

    scheme_name = putty_color_dict.get('scheme-name', 'unnamed')
    color_dict = {}  # NOTE unused
    template_dict = {}
    template_dict = {
        'scheme-name': scheme_name,
        'scheme-author': 'AUTHOR_HERE',
        'scheme-slug': scheme_name,
    }

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

    for entry in list(template_dict.keys()):
        template_dict[entry.replace('-', '_')] = template_dict[entry]

    stache = UglyMustache()
    #print('%s' % UglyMustache.render(template_str, template_dict))  # classmethod
    return stache.render(template_str, template_dict)
