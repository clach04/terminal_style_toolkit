#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""(Partially) convert a pywal template into one that can be used with tstk

pywal16 - https://github.com/eylles/pywal16.git
tstk - terminal_style_toolkit
"""

import os
import sys


#pywal template variables to mustache
mappings = {
    "foreground": "{{Colour0-hex}}",
    "background": "{{Colour2-hex}}",
    "cursor": "{{Colour5-hex}}",

    "color0": "{{Colour6-hex}}",
    "color1": "{{Colour8-hex}}",
    "color2": "{{Colour10-hex}}",
    "color3": "{{Colour12-hex}}",
    "color4": "{{Colour14-hex}}",
    "color5": "{{Colour16-hex}}",
    "color6": "{{Colour18-hex}}",
    "color7": "{{Colour20-hex}}",
    "color8": "{{Colour7-hex}}",
    "color9": "{{Colour9-hex}}",
    "color10": "{{Colour11-hex}}",
    "color11": "{{Colour13-hex}}",
    "color12": "{{Colour15-hex}}",
    "color13": "{{Colour17-hex}}",
    "color14": "{{Colour19-hex}}",
    "color15": "{{Colour21-hex}}",
}


def main(argv=None):
    argv = argv or sys.argv
    #print('Python %s on %s' % (sys.version, sys.platform))

    template_filename = argv[1]

    f = open(template_filename)  # just assume this will work, correct text mode and encoding - assume utf-8
    template_str = f.read()
    f.close()

    for entry in mappings:
        new_variable = mappings[entry]
        template_str = template_str.replace('{%s}' % entry, new_variable)
        new_variable = new_variable.replace('-hex', '-rgb-r') + ',' + new_variable.replace('-hex', '-rgb-g') + ',' + new_variable.replace('-hex', '-rgb-b')
        template_str = template_str.replace('{%s.rgb}' % entry, new_variable)

    print('%s' % template_str)

    return 0

if __name__ == "__main__":
    sys.exit(main())
