#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""(Partially?) convert a Base24 color scheme/theme YAML file into json (to stdout) that can be used with tstk

Base24 spec https://github.com/tinted-theming/base24/blob/main/styling.md
Also see Base16 spec - https://github.com/tinted-theming/home/blob/main/styling.md
"""

import os
import json
import sys

# This is (so far...) the only script that needs external dependencies

try:
    import oyaml as yaml
except ImportError:
    import yaml  # pyyaml
# TODO strictyaml - built in solution to the Norway problem...


# TODO
mapping = {
    "name": "scheme-name",
    "author": "scheme-author",
}

"""TODO - AKA unused...
     Colour1-hex: "Default Bold Foreground  -- equals to non-bold",
     Colour3-hex: "Default Bold Background  -- equals to non-bold",
     Colour4-hex: "Cursor Text -- equals to default background",
     Colour5-hex: "Cursor Colour -- equals to default foreground",
"""
color_mapping = {
    # Assuming dark "variant"
    "base00": "Colour2-hex",  # Background   - Default Background
    "base01": "Colour6-hex",  # Black        - Lighter Background (Used for status bars)
    "base02": "Colour7-hex",  # Bright Black - Selection Background
    #"base03": "FIXME03",  # (Grey)       - Comments, Invisibles, Line Highlighting
    #"base04": "FIXME04",  # (Light Grey) - Dark Foreground (Used for status bars)
    "base05": "Colour0-hex",  # Foreground   - Default Foreground, Caret, Delimiters, Operators
    "base06": "Colour20-hex",  # White        - Light Foreground (Not often used)
    "base07": "Colour21-hex",  # Bright White - The Lightest Foreground (Not often used)

    # Colors - Base16
    "base08": "Colour8-hex",  # Red 
    #"base09": "FIXME09",  # (Orange) 
    "base0A": "Colour12-hex",  # Yellow 
    "base0B": "Colour10-hex",  # Green 
    "base0C": "Colour18-hex",  # Cyan 
    "base0D": "Colour14-hex",  # Blue 
    "base0E": "Colour16-hex",  # Magenta 
    #"base0F": "FIXME0F",  # (Dark Red or Brown)

    # Colors - Base24 - ANSI bright
    #"base10": "FIXME10",  # (Darker Black) 
    #"base11": "FIXME11",  # (Darkest Black) ?? Wonder if Colour1-hex: "Default Bold Foreground  -- equals to non-bold" could work?
    "base12": "Colour9-hex",  # Bright Red 
    "base13": "Colour13-hex",  # Bright Yellow 
    "base14": "Colour11-hex",  # Bright Green 
    "base15": "Colour19-hex",  # Bright Cyan 
    "base16": "Colour15-hex",  # Bright Blue 
    "base17": "Colour17-hex"   # Bright Magenta 
}

def reverse_mapping():
    reverse_mapping_dict = {}
    for entry_name in mapping:
        reverse_mapping_dict[mapping[entry_name]] = entry_name

    # base00-base07 - may need reverse mapping depending on "variant" - at least for light (TODO list and reverse....)
    for entry_name in color_mapping:
        reverse_mapping_dict[color_mapping[entry_name]] = entry_name

    return reverse_mapping_dict

def read_yaml_file(in_filename):
    f = open(in_filename)  # just assume this will work, correct text mode and encoding - assume utf-8
    #result_dict = yaml.safe_load(f)
    result_dict = yaml.load(f, Loader=yaml.BaseLoader)  # resolve the Norway problem
    f.close()
    return result_dict

def read_and_convert_base24_yaml(in_filename):
    color_theme = {}
    color_theme["scheme-comment"] = "Base24 import of %s" % (in_filename.replace('"', "'"))

    base24_scheme = read_yaml_file(in_filename)

    #print(base24_scheme)
    #print('-' * 65)
    #print('%s' % json.dumps(base24_scheme, indent=4)) 
    #print('-' * 65)
    assert base24_scheme["system"] == "base24"  # TODO make this an if, asserts can be optimized away...

    if base24_scheme.get("slug"):
        color_theme["scheme-slug"] = base24_scheme["slug"]  # Base16, not expected to see this for Base24
    # else default using regular slug generation, outside of this function

    """
    # DEBUG init - make it easier to spot unfilled in colors
    #hex_rgb = "deadbe"  # example; ffffff
    hex_rgb = "FIXME"  # example; ffffff
    #hex_rgb = "FFA8EB"  # bright pink
    for color_number in range(21 +1):
        color_string_prefix = 'Colour%d' % color_number
        hex_lookup_name = '%s-hex' % color_string_prefix
        color_theme[hex_lookup_name] = hex_rgb
    """

    for entry_name in mapping:
        color_theme[mapping[entry_name]] = base24_scheme[entry_name]

    # base00-base07 - just use, as-is? Could need reverse mapping depending on "variant" - at least for light (TODO list and reverse....)
    #base24_scheme["variant"] == "dark"
    for entry_name in color_mapping:
        color_theme[color_mapping[entry_name]] = base24_scheme["palette"][entry_name]


    # Generic default missing items - Could be extended to help with Base16
    color_theme["Colour1-hex"] = color_theme.get("Colour1-hex", color_theme["Colour0-hex"])  # Default Bold Foreground  -- equals to non-bold
    color_theme["Colour3-hex"] = color_theme.get("Colour3-hex", color_theme["Colour2-hex"])  # Default Bold Background  -- equals to non-bold
    color_theme["Colour4-hex"] = color_theme.get("Colour4-hex", color_theme["Colour2-hex"])  # Cursor Text -- equals to default background
    color_theme["Colour5-hex"] = color_theme.get("Colour5-hex", color_theme["Colour0-hex"])  # Cursor Colour -- equals to default foreground

    return color_theme

def main(argv=None):
    argv = argv or sys.argv
    #print('Python %s on %s' % (sys.version, sys.platform))

    theme_filename = argv[1]
    color_theme = read_and_convert_base24_yaml(theme_filename)

    print('%s' % json.dumps(color_theme, indent=4))  # TODO sort, also consider using render - or use any2theme.py
    #print('%s' % json.dumps(reverse_mapping(), indent=4, sort_keys=True))  # DEBUG

    return 0

if __name__ == "__main__":
    sys.exit(main())
