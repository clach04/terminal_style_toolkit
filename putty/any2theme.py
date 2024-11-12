#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Accept multiple formats in:

    Putty registry export
    tstk

TODO
    pywal16 json
    iterm2 xml
    gogh json
    alacritty yaml/yml
    alacritty toml
    
"""

import json
import optparse
import os
import sys

import putty_colors_render_template
import putty_reg2json


version_tuple = __version_info__ = (0, 0, 1, 'dev1')  # pep-440
version = version_string = __version__ = '.'.join(map(str, __version_info__))


class MyParser(optparse.OptionParser):
    def format_epilog(self, formatter):
        """Preserve newlines present in epilog parameter to OptionParser"""
        return self.expand_prog_name(self.epilog or '')


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = MyParser(
        usage="usage: %prog [options] input_file_name",
        version="%%prog %s" % __version__,
        description="Process theme colors into a theme for a specific tool/format",
        epilog="""
Examples:

    any2theme.py...
"""
    )
    parser.add_option("-o", "--output", help="Filename to output to (if not set use slug name. TODO what about extension?), use '-' for stdout", default="-")
    parser.add_option("-r", "--raw", help="Output raw tstk json, unprocess. Ignore template", action="store_true")
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

    in_filename = args[0]
    template_filename = options.template or 'putty_reg.mustache'  # TODO review default to Putty registry output
    in_filename_lower = in_filename.lower()
    in_filename_exten = os.path.splitext(in_filename_lower)[-1]

    # TODO override input format on command line
    # TODO determine format from filename extension and/or file contents
    if in_filename_lower.endswith('.tstk'):
        f = open(in_filename, 'r')
        x = f.read()
        f.close()

        # FIXME assume tstk json input
        color_dict = json.loads(x)
    elif in_filename_lower.endswith('.reg'):
        # TODO refactor into putty_reg2json
        config_entry = []
        # Simplistic registry file reader, assumes single byte or utf8 (i.e. not UCS2/UTF-16)
        # Ignores key names, only looks at values
        for line in putty_reg2json.get_lines_from_file(in_filename, putty_reg2json.get_all_lines, mode='r'):
            if line.startswith('"') or line.startswith('['):
                config_entry.append(line)

        include_optional_values = False
        #include_optional_values = True

        color_dict = {}
        for line in config_entry:
            if line.startswith('[HKEY_CURRENT_USER\\Software\\SimonTatham\\PuTTY\\Sessions\\'):
                #print('GOT %r' % line)
                putty_session_name = line.rsplit('\\', 1)[-1]
                putty_session_name = putty_session_name[:-1]
                #print('GOT %r' % putty_session_name)
                color_dict['scheme-slug'] = color_dict['scheme-name'] = putty_session_name
                continue
            elif not line.startswith('"Colour'):
                #print('; IGNORED: %s' % line)  # TODO make this configurable?
                continue
            # NOTE assumes Color.... - no filtering..
            #print(line)
            #print(shlex.split(line)[0].split('='))
            color_number, decimal_rgb = putty_reg2json.shlex.split(line)[0].split('=')
            #print(color_number, decimal_rgb)
            r, g, b = map(int, decimal_rgb.split(','))
            # print('%s %s %d,%d,%d #%02x %02x %02x ' % (color_number, decimal_rgb, r, g, b, r, g, b))
            #print('; #%02x%02x%02x ' % (r, g, b))
            #print(line)
            color_dict[color_number] = '%d,%d,%d' % (r, g, b)  # Decimal RGB, as used by Putty
            # Optional
            if include_optional_values:  # skip this, process will handle this later if not using raw - FIXME diff comment from putty_reg2json
                color_dict['%s-hex' % color_number] = '%02x%02x%02x' % (r, g, b)  # Hex RGB
                color_dict['%s-rgb-r' % color_number] = r
                color_dict['%s-rgb-g' % color_number] = g
                color_dict['%s-rgb-b' % color_number] = b


        f = open(in_filename, 'r')
        x = f.read()
        f.close()

        putty_reg2json
    else:
        raise NotImplementedError('TODO unknown input format %r' % (in_filename_exten,))

    if options.output != '-':
        #raise NotImplementedError('TODO non-stdout')
        f_out = open(options.output, 'w')
    else:
        f_out = sys.stdout
    if options.raw:
        # TODO not sure about writing text/strings to stdout...
        f_out.write('%s' % json.dumps(color_dict, indent=4))  # , sort_keys=True))  # sorting order is not natural :-(
        return 0

    template_dict = putty_colors_render_template.process_theme(color_dict, guess_theme_name=os.path.basename(in_filename))
    # TODO / FIXME slug-name URI escape processing

    if options.raw:
        f_out.write('%s' % json.dumps(template_dict, indent=4))  # NOT sure about this...
        return 0

    # TODO / FIXME slug-name URI escape processing
    # FIXME detect missing colors?
    output = putty_colors_render_template.render_template(template_dict, template_filename, process_dict=False)  # TODO see comment above, add sanity check parameter
    # FIXME template filename output...
    f_out.write('%s' % output)

    if options.output != '-':
        f_out.close()


    return 0


if __name__ == "__main__":
    sys.exit(main())
