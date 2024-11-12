#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Convert a Windows registry export of a single Putty session into a json (theme) file to stdout

Expects single byte or utf-8 encoded file, for example, UCS2/UTF-16 is NOT supported
"""

# Clone of putty_reg_file_to_sorted.py - todo refactor and share code
import json
import re
import shlex
import sys

try:
    basestring
except NameError:
    try:
        basestring = (str, unicode)
    except NameError:
        basestring = str


def get_all_lines(readobject):
    for line in readobject:
        line = line.strip()
        yield line

def get_lines_from_file(fileinfo, filer_iterator=None, mode='rb'):
    filer_iterator = filer_iterator or get_lines
    if isinstance(fileinfo, basestring):
        fileptr = open(fileinfo, mode)
    else:
        fileptr = fileinfo
    
    return filer_iterator(fileptr)

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


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

# FIXME / TODO refactor main() code below into reusable/callable function
def main(argv=None):
    if argv is None:
        argv = sys.argv

    filename = sys.argv[1]
    strip_comments = True

    config_entry = []
    # Simplistic registry file reader, assumes single byte or utf8 (i.e. not UCS2/UTF-16)
    # Ignores key names, only looks at values
    for line in get_lines_from_file(filename, get_all_lines, mode='r'):
        if line.startswith('"') or line.startswith('['):
            config_entry.append(line)

    #config_entry.sort()
    config_entry = natural_sort(config_entry)

    template_dict = {}
    template_dict = {
        'scheme-name': 'NAME_HERE',
        'scheme-author': 'AUTHOR_HERE',
        'scheme-slug': 'SLUG_HERE',
    }

    include_optional_values = False
    include_optional_values = True

    for line in config_entry:
        if line.startswith('[HKEY_CURRENT_USER\\Software\\SimonTatham\\PuTTY\\Sessions\\'):
            #print('GOT %r' % line)
            putty_session_name = line.rsplit('\\', 1)[-1]
            putty_session_name = putty_session_name[:-1]
            #print('GOT %r' % putty_session_name)
            template_dict['scheme-slug'] = template_dict['scheme-name'] = putty_session_name
            continue
        elif not line.startswith('"Colour'):
            #print('; IGNORED: %s' % line)  # TODO make this configurable?
            continue
        # NOTE assumes Color.... - no filtering..
        #print(line)
        shlex.shlex
        #print(shlex.split(line)[0].split('='))
        color_number, decimal_rgb = shlex.split(line)[0].split('=')
        #print(color_number, decimal_rgb)
        r, g, b = map(int, decimal_rgb.split(','))
        # print('%s %s %d,%d,%d #%02x %02x %02x ' % (color_number, decimal_rgb, r, g, b, r, g, b))
        #print('; #%02x%02x%02x ' % (r, g, b))
        #print(line)
        template_dict[color_number] = '%d,%d,%d' % (r, g, b)  # Decimal RGB, as used by Putty
        # Optional
        if include_optional_values:
            template_dict['%s-hex' % color_number] = '%02x%02x%02x' % (r, g, b)  # Hex RGB
            template_dict['%s-rgb-r' % color_number] = r
            template_dict['%s-rgb-g' % color_number] = g
            template_dict['%s-rgb-b' % color_number] = b

    if include_optional_values:
        # TODO review this, potentially rename to -putty (see mustache template for tstk)
        template_dict.update({
            "Colour0-comment": "Default Foreground",
            "Colour1-comment": "Default Bold Foreground  -- equals to non-bold",
            "Colour2-comment": "Default Background",
            "Colour3-comment": "Default Bold Background  -- equals to non-bold",
            "Colour4-comment": "Cursor Text -- equals to default background",
            "Colour5-comment": "Cursor Colour -- equals to default foreground",
            "Colour6-comment": "ANSI Black - 30m / 40m",
            "Colour7-comment": "ANSI Black Bright - 1;30m",
            "Colour8-comment": "ANSI Red - 31m / 41m",
            "Colour9-comment": "ANSI Red Bright - 1;31m",
            "Colour10-comment": "ANSI Green - 32m / 42m",
            "Colour11-comment": "ANSI Green Bright - 1;32m",
            "Colour12-comment": "ANSI Yellow - 33m / 43m",
            "Colour13-comment": "ANSI Yellow Bright - 1;33m",
            "Colour14-comment": "ANSI Blue - 34m / 44m",
            "Colour15-comment": "ANSI Blue Bright - 1;34m",
            "Colour16-comment": "ANSI Magenta - 35m / 45m",
            "Colour17-comment": "ANSI Magenta Bright - 1;35m",
            "Colour18-comment": "ANSI Cyan - 36m / 46m",
            "Colour19-comment": "ANSI Cyan Bright - 1;36m",
            "Colour20-comment": "ANSI White - 37m / 47m",
            "Colour21-comment": "ANSI White Bright - 1;37m",
        })
    #print(';' * 65)
    #print('')
    # Dump json to stdout
    print('%s' % json.dumps(template_dict, indent=4))
    #print('%s' % json.dumps(template_dict, indent=4, sort_keys=True))  # sorting order is no natural :-(

    return 0


if __name__ == "__main__":
    sys.exit(main())
