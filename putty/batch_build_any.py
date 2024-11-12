#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

import glob
import os
import sys

#import putty_colors_render_template
import any2theme

version_tuple = __version_info__ = (0, 0, 1, 'dev1')  # pep-440
version = version_string = __version__ = '.'.join(map(str, __version_info__))

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = any2theme.MyParser(
        usage="usage: %prog [options] input_pattern1 [input_pattern2] [input_pattern3]",
        version="%%prog %s" % __version__,
        description="Batch process theme colors into a theme for a specific tool/format",
        epilog="""
Examples:

    py -3 batch_build_any.py --output_extension .reg *.tstk
    py -3 batch_build_any.py --output_extension .tstk -t terminal_style_toolkit_json.mustache *.reg
    py -3 batch_build_any.py --output_extension .tstk -t terminal_style_toolkit_json.mustache *.tstk
    py -3 batch_build_any.py --output_extension "" -t mintty_theme.mustache *.tstk
"""
    )
    parser.add_option("--output-extension", "--output_extension", help="Output filename extension")
    parser.add_option("-t", "--template", help="Filename of template to use")  # default to tstk or putty?
    parser.add_option("-v", "--verbose", help='Verbose output', action="store_true")
    # TODO add force input format option

    (options, args) = parser.parse_args(argv[1:])
    #import pdb; pdb.set_trace()
    verbose = options.verbose
    if verbose:
        print('Python %s on %s' % (sys.version.replace('\n', ' - '), sys.platform))
    if not args:
        parser.print_usage()
        return 1

    template_filename = options.template or 'putty_reg.mustache'  # TODO review default to Putty registry output
    for pattern in args:
        for in_filename in glob.glob(pattern):
            any2theme.main(['batch_build_any', "--template", template_filename, "--output_extension", options.output_extension, in_filename])

    return 0


if __name__ == "__main__":
    sys.exit(main())

