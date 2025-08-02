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


def derive_21_from_8_bright_as_copy(color_dict):
    # TODO copy color_dict to avoid side effects
    default_mapping_if_missing = putty_colors_render_template.default_mapping_if_missing

    for color_number in range(21 +1):
        color_string_prefix = 'Colour%d' % color_number
        # ONLY check for hex
        hex_lookup_name = '%s-hex' % color_string_prefix
        hex_rgb = color_dict.get(hex_lookup_name)
        if not hex_rgb:
            copy_color_name = default_mapping_if_missing[hex_lookup_name]
            color_dict[hex_lookup_name] = color_dict[copy_color_name]
            comment_lookup_name = '%s-comment' % color_string_prefix
            color_dict[comment_lookup_name] = "Copied from %s" % (copy_color_name,)

    # TODO (if not set,) set "scheme-comment" (or "scheme-comment1-9" - which ever is the first empty slot) with "generated from ...." note
    return color_dict


def main(argv=None):
    if argv is None:
        argv = sys.argv

    in_filename = argv[1]
    f = open(in_filename, 'r')  # assume no encoding issues...
    x = f.read()
    f.close()
    color_dict = json.loads(x)

    derive_21_from_8 = derive_21_from_8_bright_as_copy  # TODO implement a brighten/lighten generator
    color_theme = derive_21_from_8(color_dict)
    #print('%s' % json.dumps(color_theme, indent=4))  # TODO sort, also consider using render - or use any2theme.py
    print('%s' % json.dumps(color_theme, indent=4, sort_keys=True))  # TODO consider using render - or use any2theme.py

    return 0


if __name__ == "__main__":
    sys.exit(main())
