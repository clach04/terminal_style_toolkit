#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""(Partially?) convert an Alacritty color theme TOML file into json (to stdout) that can be used with tstk

Ignore dark/dim
assume normal and bright/bold present

Example Usage:

    py -3 alacritty_toml2tstk_json.py  dracula.toml > alacritty_dracula_tstk.json
    py -3 putty/json2putty_reg.py alacritty_dracula_tstk.json putty/terminal_style_toolkit_json.mustache alacritty_dracula.tstk
    py -3 putty/json2putty_reg.py alacritty_dracula.tstk

NOTE in dracula demo, differences from spec:

  * Black
  * Black Bright
  * Red Bright
  * Green Bright
  * Yellow Bright
  * Blue Bright
  * Magenta Bright
  * Cyan Bright
  * White

"""

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os
import json
import sys




mapping = {
    "colors.primary": {
        "background": "Colour2-hex",  # Default Background
        "foreground": "Colour0-hex"   # Default Foreground
    },
    "colors.normal": {
        "black":    "Colour6-hex",
        "red":      "Colour8-hex",
        "green":    "Colour10-hex",
        "yellow":   "Colour12-hex",
        "blue":     "Colour14-hex",
        "magenta":  "Colour16-hex",
        "cyan":     "Colour18-hex",
        "white":    "Colour20-hex",
    },
    "colors.bright": {
        "black":    "Colour7-hex",
        "red":      "Colour9-hex",
        "green":    "Colour11-hex",
        "yellow":   "Colour13-hex",
        "blue":     "Colour15-hex",
        "magenta":  "Colour17-hex",
        "cyan":     "Colour19-hex",
        "white":    "Colour21-hex",
    }
}

def main(argv=None):
    argv = argv or sys.argv
    #print('Python %s on %s' % (sys.version, sys.platform))

    theme_filename = argv[1]
    color_theme = {}

    """
    f = open(theme_filename)  # just assume this will work, correct text mode and encoding - assume utf-8
    template_str = f.read()
    f.close()
    """

    # treat alacritty toml as an init file (as of 2024-09-15 current format is ini compatible), so no need for external libs
    config = configparser.ConfigParser()
    config.read(theme_filename)  # FIXME what if file is missing, unreadable, etc. TODO sanity check needed


    #config_section_name = 'colors.primary'  # or pick first one; config.sections()[0]
    for config_section_name in mapping.keys():
        try:
            for alacritty_color_name in config.options(config_section_name):
                #print('%s\t%s' % (alacritty_color_name, config.get(config_section_name, alacritty_color_name)))
                rgb_hex = config.get(config_section_name, alacritty_color_name)
                rgb_hex = rgb_hex.replace('#', '')  # remove leading '#'
                rgb_hex = rgb_hex.replace('0x', '')  # remove leading '0x'
                rgb_hex = rgb_hex.replace('"', '')  # remove double quotes
                rgb_hex = rgb_hex.replace("'", '')  # remove single quotes
                #mapping[config_section_name][alacritty_color_name] = 'FIXME'
                tstk_color_name = mapping[config_section_name][alacritty_color_name]
                color_theme[tstk_color_name] = rgb_hex
        except configparser.NoSectionError:
            pass

    """Python3 only
    print(config.sections())  # ['colors.primary', 'colors.normal', 'colors.bright']
    print(config['colors.primary'])  # nothing useful displayed
    print(config['colors.primary']['background'])  # useful, #hex_rgb_8_bit
    """

    # TODO idea loop through and default missing items?
    color_theme["Colour1-hex"] = color_theme.get("Colour1-hex", color_theme["Colour0-hex"])  # Default Bold Foreground  -- equals to non-bold
    color_theme["Colour3-hex"] = color_theme.get("Colour3-hex", color_theme["Colour2-hex"])  # Default Bold Background  -- equals to non-bold
    color_theme["Colour4-hex"] = color_theme.get("Colour4-hex", color_theme["Colour2-hex"])  # Cursor Text -- equals to default background
    color_theme["Colour5-hex"] = color_theme.get("Colour5-hex", color_theme["Colour0-hex"])  # Cursor Colour -- equals to default foreground

    color_theme["scheme-name"] = os.path.basename(theme_filename)  ## filename as a starting point, will need manually editing later

    print('%s' % json.dumps(color_theme, indent=4))  # TODO sort, also consider using render
    #print('%s' % json.dumps(mapping, indent=4))  # TODO sort, also consider using render
    #print('%s' % json.dumps(mapping, indent=4, sort_keys=True))  # TODO sort, also consider using render

    return 0

if __name__ == "__main__":
    sys.exit(main())
