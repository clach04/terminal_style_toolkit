#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Display Putty 21 colors in a bar on the console/terminal
"""

import glob
import json
import logging
import os
import sys

import putty_colors_render_template

is_win = sys.platform.startswith('win')


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
        f = open(filename, 'r')  # assume no encoding issues...
        x = f.read()
        f.close()
        color_dict = json.loads(x)

        putty_colors_render_template.print_colors_terminal(color_dict)
        print("  %s" % (filename,))  # TODO theme name

    print('%d files' % len(filenames))

    return 0


if __name__ == "__main__":
    sys.exit(main())
