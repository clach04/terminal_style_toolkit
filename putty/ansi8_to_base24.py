#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""derive bg/fg colors base00-base07 https://github.com/tinted-theming/base24/blob/main/styling.md

    python ansi8_to_base24.py ../docs/sample_ansi8.tstk
"""

import glob
import json
import logging
import os
import sys

"""# NOT needed yet
try:
    import oyaml as yaml
except ImportError:
    import yaml  # pyyaml
# TODO strictyaml - built in solution to the Norway problem...
"""

import console_view_base24
import putty_colors_render_template

def increase_by_factor(x, factor):
    return int(min(max(x + factor, 0), 255))

def generate_base00_base07(bg_color_hex='#000000', fg_color_hex='#ffffff'):
    if not bg_color_hex.startswith('#'): bg_color_hex = '#' + bg_color_hex
    if not fg_color_hex.startswith('#'): fg_color_hex = '#' + fg_color_hex

    hex2rgb_ints = putty_colors_render_template.hex2rgb_ints
    bg_color_rgb_ints = hex2rgb_ints(bg_color_hex)
    fg_color_rgb_ints = hex2rgb_ints(fg_color_hex)
    #print(bg_color_rgb_ints)
    #print(fg_color_rgb_ints)

    # TODO determine direction - this assumes dark (background) to light (foreground)
    r_factor = (fg_color_rgb_ints[0] - bg_color_rgb_ints[0]) / 6
    g_factor = (fg_color_rgb_ints[1] - bg_color_rgb_ints[1]) / 6
    b_factor = (fg_color_rgb_ints[2] - bg_color_rgb_ints[2]) / 6

    #print((fg_color_rgb_ints[0] - bg_color_rgb_ints[0]) / 6)
    #print((fg_color_rgb_ints[1] - bg_color_rgb_ints[1]) / 6)
    #print((fg_color_rgb_ints[2] - bg_color_rgb_ints[2]) / 6)

    result_palette = {}
    for x in range(7 + 1):
        #print('base%02d: %r' % (x, bg_color_rgb_ints[0] + (x * (fg_color_rgb_ints[0] - bg_color_rgb_ints[0]) / 6)) )
        new_rgb = (increase_by_factor(bg_color_rgb_ints[0], x * r_factor), increase_by_factor(bg_color_rgb_ints[1], x * g_factor), increase_by_factor(bg_color_rgb_ints[2], x * b_factor))
        #print('base%02d: %r' % (x, new_rgb) )
        #print('base%02d: %r' % (x, '#%02x%02x%02x' % new_rgb) )  # Hex RGB
        result_palette['base%02d' % (x,)] = '#%02x%02x%02x' % new_rgb

    # TODO review saity check
    assert result_palette["base00"] == bg_color_hex
    assert result_palette["base06"] == fg_color_hex

    return result_palette


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version.replace('\n', ' '), sys.platform.replace('\n', ' ')))

    in_filename = argv[1]
    tstk_theme8 = putty_colors_render_template.read_json_file(in_filename)
    bg_color_hex = tstk_theme8["Colour6-hex"]  # ANSI Black - 30m / 40m
    fg_color_hex = tstk_theme8["Colour20-hex"]  # ANSI White - 37m / 47m
    #generate_base00_base07()  # TODO params
    base00_base07 = generate_base00_base07(bg_color_hex=bg_color_hex, fg_color_hex=fg_color_hex)
    #print(base00_base07)  # DEBUG
    #color_names = list(base24_scheme["palette"].keys())
    color_names = list(base00_base07.keys())
    color_names.sort()
    #console_view_base24.print_listed_colors_terminal(base00_base07, color_names) ; print('')  # DEBUG

    derive_21_from_8 = putty_colors_render_template.derive_21_from_8_bright  # base bright colors on base colors
    tstk_theme = derive_21_from_8(tstk_theme8)
    #putty_colors_render_template.print_colors_terminal(tstk_theme) ; print('')  # DEBUG

    base24_scheme = {
        "system": "base24",
        "name": tstk_theme.get("scheme-name", "FIXME"),
        "author": tstk_theme.get("scheme-author", "FIXME"),
        "variant": "dark",  # Also a FIXME
        "palette": base00_base07,
    }
    base24_scheme["palette"].update({
        # Colors - Base16
        "base08": tstk_theme["Colour8-hex"],  # Red 
        #"base09": "FIXME09",  # (Orange) 
        "base0A": tstk_theme["Colour12-hex"],  # Yellow 
        "base0B": tstk_theme["Colour10-hex"],  # Green 
        "base0C": tstk_theme["Colour18-hex"],  # Cyan 
        "base0D": tstk_theme["Colour14-hex"],  # Blue 
        "base0E": tstk_theme["Colour16-hex"],  # Magenta 
        #"base0F": "FIXME0F",  # (Dark Red or Brown)

        # Colors - Base24 - ANSI bright
        #"base10": "FIXME10",  # (Darker Black) 
        #"base11": "FIXME11",  # (Darkest Black) ?? Wonder if Colour1-hex: "Default Bold Foreground  -- equals to non-bold" could work?
        "base12": tstk_theme["Colour9-hex"],  # Bright Red 
        "base13": tstk_theme["Colour13-hex"],  # Bright Yellow 
        "base14": tstk_theme["Colour11-hex"],  # Bright Green 
        "base15": tstk_theme["Colour19-hex"],  # Bright Cyan 
        "base16": tstk_theme["Colour15-hex"],  # Bright Blue 
        "base17": tstk_theme["Colour17-hex"],   # Bright Magenta 
    })

    # FIXME, temporarly use pink as not filled in color marker
    base24_scheme["palette"]["base09"] = "#FFA8EB"  # bright pink
    base24_scheme["palette"]["base0F"] = "#FFA8EB"  # bright pink
    base24_scheme["palette"]["base10"] = "#FFA8EB"  # bright pink
    base24_scheme["palette"]["base11"] = "#FFA8EB"  # bright pink

    color_names = list(base24_scheme["palette"].keys())
    color_names.sort()
    console_view_base24.print_listed_colors_terminal(base24_scheme["palette"], color_list=color_names) ; print('')
    print('%s' % json.dumps(base24_scheme, indent=4, sort_keys=True))  # json is a subset of yaml, so this is valid yaml


    return 0


if __name__ == "__main__":
    sys.exit(main())
