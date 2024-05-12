#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Import single theme json color scheme from https://github.com/Gogh-Co/Gogh/blob/master/json/

For example try with https://github.com/Gogh-Co/Gogh/blob/master/json/3024-day.json as input file
"""

import os
import sys

import parse_palette_tools


def gogh_color_dict2putty_color_dict(gogh_color_dict):
    """Schema and notes

        color_01: '#050404'    # Black (Host)
        color_02: '#BD0013'    # Red (Syntax string)
        color_03: '#4AB118'    # Green (Command)
        color_04: '#E7741E'    # Yellow (Command second)
        color_05: '#0F4AC6'    # Blue (Path)
        color_06: '#665993'    # Magenta (Syntax var)
        color_07: '#70A598'    # Cyan (Prompt)
        color_08: '#F8DCC0'    # White

        color_09: '#4E7CBF'    # Bright Black
        color_10: '#FC5F5A'    # Bright Red (Command error)
        color_11: '#9EFF6E'    # Bright Green (Exec)
        color_12: '#EFC11A'    # Bright Yellow
        color_13: '#1997C6'    # Bright Blue (Folder)
        color_14: '#9B5953'    # Bright Magenta
        color_15: '#C8FAF4'    # Bright Cyan
        color_16: '#F6F5FB'    # Bright White

        background: '#1F1D45'  # Background
        foreground: '#F8DCC0'  # Foreground (Text)

        cursor: '#F8DCC0'      # Cursor
    """
    for key_name in list(gogh_color_dict.keys()):
        if gogh_color_dict[key_name].startswith('#'):  # Assume we have a color...
            gogh_color_dict[key_name] = parse_palette_tools.hex2rgb_string_decimal_ints_commas(gogh_color_dict[key_name])

    putty_color_dict = {
        "scheme-name" : gogh_color_dict['name'],
        "#comment" : "Comment_goes_here",

        "#CommentColor" : "Decimal r,g,b - with no spaces",

        "Colour0" : gogh_color_dict['foreground'],
        "#" : "Default Foreground",

        "Colour1" : gogh_color_dict['foreground'],  # TODO REVIEW
        "#" : "Default Bold Foreground",

        "Colour2" : gogh_color_dict['background'],
        "#" : "Default Background",

        "Colour3" : gogh_color_dict['background'],  # TODO REVIEW
        "#" : "Default Bold Background",

        "Colour4" : gogh_color_dict['foreground'],  # TODO REVIEW
        "#" : "Cursor Text",

        "Colour5" : gogh_color_dict['cursor'],  # TODO review
        "#" : "Cursor Colour",

        "Colour6" : gogh_color_dict['color_01'],
        "#" : "ANSI Black - 30m / 40m",

        "Colour7" : gogh_color_dict['color_09'],
        "#" : "ANSI Black Bright- 1;30m",

        "Colour8" : gogh_color_dict['color_02'],
        "#" : "ANSI Red - 31m / 41m",

        "Colour9" :  gogh_color_dict['color_10'],
        "#" : "ANSI Red Bright - 1;31m",

        "Colour10" : gogh_color_dict['color_03'],
        "#" : "ANSI Green - 32m / 42m",

        "Colour11" : gogh_color_dict['color_11'],
        "#" : "ANSI Green Bright - 1;32m",

        "Colour12" : gogh_color_dict['color_04'],
        "#" : "ANSI Yellow - 33m / 43m",

        "Colour13" : gogh_color_dict['color_12'],
        "#" : "ANSI Yellow Bright - 1;33m",

        "Colour14" : gogh_color_dict['color_05'],
        "#" : "ANSI Blue - 34m / 44m",

        "Colour15" : gogh_color_dict['color_13'],
        "#" : "ANSI Blue Bright - 1;34m",

        "Colour16" : gogh_color_dict['color_06'],
        "#" : "ANSI Magenta - 35m / 45m",

        "Colour17" : gogh_color_dict['color_14'],
        "#" : "ANSI Magenta Bright - 1;35m",

        "Colour18" : gogh_color_dict['color_07'],
        "#" : "ANSI Cyan - 36m / 46m",

        "Colour19" : gogh_color_dict['color_15'],
        "#" : "ANSI Cyan Bright - 1;36m",

        "Colour20" : gogh_color_dict['color_08'],
        "#" : "ANSI White - 37m / 47m",

        "Colour21" : gogh_color_dict['color_16'],
        "#" : "ANSI White Bright - 1;37m"
    }
    # ignore hash

    #putty_color_dict['scheme-name'] = gogh_color_dict['name']
    #putty_color_dict['XXX'] = gogh_color_dict['XXX']

    """
    # ignore hash

    # color_X -> ColourX
    putty_color_dict['Colour0'] = gogh_color_dict['foreground']
    putty_color_dict['Colour2'] = gogh_color_dict['background']
    putty_color_dict['Colour5'] = gogh_color_dict['cursor']  # TODO review
    """

    return putty_color_dict


def main(argv=None):
    argv = argv or sys.argv
    print('Python %s on %s' % (sys.version, sys.platform))

    filename = argv[1]
    gogh_color_dict = parse_palette_tools.json_reader(filename)
    putty_color_dict = gogh_color_dict2putty_color_dict(gogh_color_dict)
    out_filename = filename + '_putty.json'
    print('Writting to %s putty format json' % out_filename)
    parse_palette_tools.json_writer(out_filename, putty_color_dict)

    return 0

if __name__ == "__main__":
    sys.exit(main())
