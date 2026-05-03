#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Given 8 ANSI colors (currently only support TSTK as input) generate full TSTK colors
"""

import json
import logging
import os
import sys

import putty_colors_render_template


log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(level=logging.INFO)
#log.setLevel(level=logging.DEBUG)




def main(argv=None):
    if argv is None:
        argv = sys.argv

    in_filename = argv[1]
    f = open(in_filename, 'r')  # assume no encoding issues...
    x = f.read()
    f.close()
    color_dict = json.loads(x)

    #derive_21_from_8 = putty_colors_render_template.derive_21_from_8_bright_as_copy  # simply copy to "bright" colors
    derive_21_from_8 = putty_colors_render_template.derive_21_from_8_bright  # base bright colors on base colors
    color_theme = derive_21_from_8(color_dict)
    #print('%s' % json.dumps(color_theme, indent=4))  # TODO sort, also consider using render - or use any2theme.py
    print('%s' % json.dumps(color_theme, indent=4, sort_keys=True))  # TODO consider using render - or use any2theme.py

    return 0


if __name__ == "__main__":
    sys.exit(main())
