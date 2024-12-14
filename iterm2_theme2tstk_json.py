#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Partially convert an Iterm2 color theme XML file into json (to stdout) that can be used with tstk

Result will need editing to be complete. For example;
  * name
  * author
  * slug

Also review:

    "Colour3-hex" Default Bold Background  -- equals to non-bold

tstk - terminal_style_toolkit

Sample:

    py -2 iterm2_theme2tstk_json.py "3024 Day.itermcolors" > 3024_Day_iterm_tstk.json
    py -3 putty/json2putty_reg.py 3024_Day_iterm_tstk.json putty/terminal_style_toolkit_json.mustache 3024_Day_iterm.tstk
    py -3 putty/json2putty_reg.py 3024_Day_iterm.tstk

"""

import os
import json
import sys
try:
    from plistlib import load as plist_load
except ImportError:
    from plistlib import readPlist as plist_load


def component_to_int(c):
    return int(float(c) * 255.0)


mappings = {
    "Background Color": "Colour2-hex",

    "Foreground Color": "Colour0-hex",
    "Bold Color": "Colour1-hex",

    "Cursor Color": "Colour5-hex",
    "Cursor Text Color": "Colour4-hex",
    "Cursor Guide Color": "FIXME",

    "Selected Text Color": "FIXME",
    "Selection Color": "FIXME",

    "Badge Color": "FIXME",
    "Link Color": "FIXME",


    "Ansi 0 Color": "Colour6-hex",
    "Ansi 1 Color": "Colour8-hex",
    "Ansi 2 Color": "Colour10-hex",
    "Ansi 3 Color": "Colour12-hex",
    "Ansi 4 Color": "Colour14-hex",
    "Ansi 5 Color": "Colour16-hex",
    "Ansi 6 Color": "Colour18-hex",
    "Ansi 7 Color": "Colour20-hex",

    "Ansi 8 Color": "Colour7-hex",
    "Ansi 9 Color": "Colour9-hex",
    "Ansi 10 Color": "Colour11-hex",
    "Ansi 11 Color": "Colour13-hex",
    "Ansi 12 Color": "Colour15-hex",
    "Ansi 13 Color": "Colour17-hex",
    "Ansi 14 Color": "Colour19-hex",
    "Ansi 15 Color": "Colour21-hex",
}
DUMP_UNMAPPED = False
IGNORE_UNKNOWN_KEYS = True

def main(argv=None):
    argv = argv or sys.argv
    #print('Python %s on %s' % (sys.version, sys.platform))

    theme_filename = argv[1]

    f = open(theme_filename, 'rb')
    iterm_theme = plist_load(f)
    f.close()


    #print('-'*65)
    #print(iterm_theme)
    #print('-'*65)

    color_theme = {}
    iterm2hex = {}

    for iterm_color_name in iterm_theme:
        r, g, b = iterm_theme[iterm_color_name]['Red Component'], iterm_theme[iterm_color_name]['Green Component'], iterm_theme[iterm_color_name]['Blue Component']
        r, g, b = component_to_int(r), component_to_int(g), component_to_int(b)
        rgb_hex = '%02x%02x%02x' % (r, g, b)
        #print(iterm_color_name , r, g, b)
        #print('%s\t#%02x%02x%02x' % (iterm_color_name, r, g, b))
        iterm2hex[iterm_color_name] = rgb_hex
        #iterm2hex[iterm_color_name] = "FIXME"
        try:
            tstk_color_name = mappings[iterm_color_name]
        except KeyError:
            if not IGNORE_UNKNOWN_KEYS:
                raise
            print('DEBUG unknown/mapped key %r' % (iterm_color_name,))
            print('DEBUG "%s": "FIXME",' % (iterm_color_name,))
        if tstk_color_name == 'FIXME' and DUMP_UNMAPPED:
            print('%s\t%s' % (iterm_color_name, tstk_color_name))
        color_theme[tstk_color_name] = rgb_hex

    # TODO idea loop through and default missing items?
    color_theme["Colour3-hex"] = color_theme.get("Colour3-hex", color_theme["Colour2-hex"])  # Default Bold Background  -- equals to non-bold

    #print('%s' % json.dumps(iterm2hex, indent=4, sort_keys=True))  # sorting order is not in natural order :-(
    #print('-'*65)
    print('%s' % json.dumps(color_theme, indent=4))  # TODO sort, also consider using render

    return 0

if __name__ == "__main__":
    sys.exit(main())
