#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
r"""Partially convert a pywal color them into one that can be used with tstk

Result will need editing to be complete. For example;
  * name
  * author
  * slug

Also review:

    "Colour1-hex" Default Bold Foreground  -- equals to non-bold
    "Colour3-hex" Default Bold Background  -- equals to non-bold
    "Colour4-hex" Cursor Text -- equals to default background

Consider running through terminal_style_toolkit_json.mustache

Sample Usage:

    py -3 pywaltheme2tstk_json.py %USERPROFILE%\.config\wal\colorschemes\dark\sunset_dream.json > sunset_dream_tstk.json
    py -3 putty/json2putty_reg.py sunset_dream_tstk.json putty/terminal_style_toolkit_json.mustache sunset_dream.tstk
    echo edit sunset_dream.tstk - see above notes
    py -3 putty/json2putty_reg.py sunset_dream.tstk
    py -3 putty/json2putty_reg.py sunset_dream.tstk putty/colortable_html.mustache sunset_dream.html

pywal16 - https://github.com/eylles/pywal16.git
tstk - terminal_style_toolkit
"""

import os
import json
import sys


#pywal template variables to tstk
mappings = {
    "foreground": "Colour0-hex",
    "background": "Colour2-hex",
    "cursor": "Colour5-hex",

    "color0": "Colour6-hex",
    "color1": "Colour8-hex",
    "color2": "Colour10-hex",
    "color3": "Colour12-hex",
    "color4": "Colour14-hex",
    "color5": "Colour16-hex",
    "color6": "Colour18-hex",
    "color7": "Colour20-hex",
    "color8": "Colour7-hex",
    "color9": "Colour9-hex",
    "color10": "Colour11-hex",
    "color11": "Colour13-hex",
    "color12": "Colour15-hex",
    "color13": "Colour17-hex",
    "color14": "Colour19-hex",
    "color15": "Colour21-hex",
}


def main(argv=None):
    argv = argv or sys.argv
    #print('Python %s on %s' % (sys.version, sys.platform))

    theme_filename = argv[1]

    f = open(theme_filename)  # just assume this will work, correct text mode and encoding - assume utf-8
    template_str = f.read()
    f.close()

    color_theme = {}
    pywal_colors = json.loads(template_str)

    for top_level in ['special', 'colors', ]:
        for entry in pywal_colors[top_level]:
            new_variable = mappings[entry]
            color_theme[new_variable] = pywal_colors[top_level][entry].replace('#', '')  # assume hex RGB (remove leading '#')

    # TODO idea loop through and default missing items?
    color_theme["Colour1-hex"] = color_theme.get("Colour1-hex", color_theme["Colour0-hex"])  # Default Bold Foreground  -- equals to non-bold
    color_theme["Colour3-hex"] = color_theme.get("Colour3-hex", color_theme["Colour2-hex"])  # Default Bold Background  -- equals to non-bold
    color_theme["Colour4-hex"] = color_theme.get("Colour4-hex", color_theme["Colour2-hex"])  # Cursor Text -- equals to default background

    print('%s' % json.dumps(color_theme, indent=4))  # TODO sort, also consider using render

    return 0

if __name__ == "__main__":
    sys.exit(main())
