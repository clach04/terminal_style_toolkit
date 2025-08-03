#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Display Base24 / Base 16 colors in a bar on the console/terminal
"""

import glob
import json
import logging
import os
import sys

try:
    import oyaml as yaml
except ImportError:
    import yaml  # pyyaml
# TODO strictyaml - built in solution to the Norway problem...

import putty_colors_render_template

is_win = sys.platform.startswith('win')


def print_listed_colors_terminal(color_dict, color_list):
    for color_name in color_list:
        hex_rgb = color_dict[color_name]
        if not hex_rgb.startswith('#'): hex_rgb = '#' + hex_rgb
        putty_colors_render_template.color_print(hex_rgb)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version.replace('\n', ' '), sys.platform.replace('\n', ' ')))

    if is_win:
        filenames = []
        for filename_pattern in argv[1:]:
            filenames += glob.glob(filename_pattern)
    else:
        filenames = argv[1:]

    print('%d files' % len(filenames))

    for filename in filenames:

        f = open(filename)  # just assume this will work, correct text mode and encoding - assume utf-8
        #base24_scheme = yaml.safe_load(f)
        base24_scheme = yaml.load(f, Loader=yaml.BaseLoader)  # resolve the Norway problem
        f.close()

        if "palette" in base24_scheme:
            # modern
            color_names = list(base24_scheme["palette"].keys())
            color_dict = base24_scheme["palette"]
        else:
            # assume Base16, legacy
            color_names = [x for x in base24_scheme.keys() if x.startswith('base')]
            color_dict = base24_scheme
        color_names.sort()
        #print(base24_scheme.keys())
        #print(color_names)
        print_listed_colors_terminal(color_dict, color_names)
        print("  %s : %s" % (os.path.basename(filename), base24_scheme.get("name", base24_scheme.get("scheme", "MISSING NAME"))))

    print('%d files' % len(filenames))

    return 0


if __name__ == "__main__":
    sys.exit(main())
