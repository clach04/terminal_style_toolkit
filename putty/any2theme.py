#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Accept multiple formats in:

    Putty registry export
    tstk

TODO
    gogh json
    alacritty yaml/yml - note potential file extension conflict with Base16 and Base24
    mintty
    foot - https://codeberg.org/dnkl/foot/src/branch/master/themes - https://github.com/clach04/terminal_style_toolkit/issues/24

"""

import json
import optparse
import os
import sys

def fake_module(name):  # Optional import
    # Fail with a clear message (possibly at an unexpected time) for module access and method/class/function
    class MissingModule(object):
        def __getattr__(self, attr):
            raise ImportError('No module named %s' % name)

        def __bool__(self):  # Not sure __nonzero__ check was working in py3
            # truthy if checks on this will fail
            return False
        __nonzero__ = __bool__

        def __call__(self, *args, **kwargs):
            raise ImportError('No module named %s' % name)
    return MissingModule()



import alacritty_reader
try:
    import base24_reader
except ImportError:
    base24_reader = fake_module('base24_reader')  # better than; base24_reader = None
import iterm2_reader
import putty_colors_render_template
import putty_reg2json
import pywal_reader


version_tuple = __version_info__ = (0, 0, 1, 'dev1')  # pep-440
version = version_string = __version__ = '.'.join(map(str, __version_info__))

# These really should be enums, but for py2.x want to keep external dependency count low
FORMAT_TSTK = 'tstk'  # terminal tool kit json
FORMAT_PUTTY = 'putty'  # Windows registry content as used by PuTTY https://www.chiark.greenend.org.uk/~sgtatham/putty/
FORMAT_ITERM2 = 'iterm2'  # iTerm2 is a terminal emulator for Mac OS X https://github.com/gnachman/iTerm2
FORMAT_ALACRITTY_TOML = 'alacritty_toml'  # Alacritty toml  # TODO old YAML
FORMAT_PYWAL = 'pywal'  # pywal16 json - https://github.com/clach04/terminal_style_toolkit/issues/11
FORMAT_BASE24 = 'base24'  # Base24 https://github.com/tinted-theming/base24/blob/main/styling.md - superset of Base16

ALL_FORMATS = []
for name in dir():
    if name.startswith('FORMAT_'):
        ALL_FORMATS.append(locals()[name])

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

    # generate Putty registry export theme to stdout
    py -3 any2theme.py some_theme.tstk

    # generate tstk theme to stdout
    py -3 any2theme.py -t terminal_style_toolkit_json.mustache some_theme.tstk
    py -3 any2theme.py -t terminal_style_toolkit_json.mustache some_theme.reg

    # generate Putty registry export
    py -3 any2theme.py some_theme.tstk --output_extension .reg

    # generate Terminal Style Toolkit json tstk file
    py -3 any2theme.py some_theme.tstk --output_extension .tstk -t terminal_style_toolkit_json.mustache

    # generate mintty theme file
    py -3 any2theme.py some_theme.tstk --output_extension "" -t mintty_theme.mustache

    py -3 any2theme.py DefaultPuttySettings_sorted.reg -r
    py -3 any2theme.py DefaultPuttySettings_sorted.reg -t terminal_style_toolkit_json.mustache

    py -3 any2theme.py myfile.json
    py -3 any2theme.py myfile.json -t putty_reg.mustache

    py -3 any2theme.py DefaultPuttySettings_sorted.reg
    py -3 any2theme.py DefaultPuttySettings_sorted.reg -t putty_reg.mustache

    py -3 any2theme.py myfile.json -t colortable_html.mustache -o out.html

    py -3 any2theme.py myfile.json -t mintty_theme.mustache -o myfile

Available Output Templates:

    terminal_style_toolkit_json.mustache    alacritty_nodim_yml.mustache
    mintty_theme.mustache                   ms_colortool_ini.mustache
    putty_reg.mustache                      pywal16_json.mustache
    colortable_html.mustache
"""
    )
    parser.add_option("-o", "--output", help="Filename to output to (if not set use slug name. TODO what about extension?), use '-' for stdout")
    parser.add_option("--output-extension", "--output_extension", help="Output filename extension, including '.', e.g. .tstk")
    parser.add_option("-i", "--input-format", "--input_format", help="Which format the input file is in (if not set, guess based on file extension)")
    parser.add_option("-l", "--list-input-formats", "--list_input_formats", help="List which input formats are supported", action="store_true")
    parser.add_option("-r", "--raw", help="Output raw tstk json, unprocess. Ignore template", action="store_true")
    parser.add_option("-t", "--template", help="Filename of template to use")  # default to tstk or putty?
    parser.add_option("-v", "--verbose", help='Verbose output', action="store_true")
    # TODO add force input format option

    (options, args) = parser.parse_args(argv[1:])
    #import pdb; pdb.set_trace()
    verbose = options.verbose
    if verbose:
        print('Python %s on %s' % (sys.version.replace('\n', ' - '), sys.platform))
    if options.list_input_formats:
        for x in ALL_FORMATS:
            print('\t%s' % (x,))
        return 0
    if not args:
        parser.print_usage()
        return 1

    in_filename = args[0]
    template_filename = options.template or 'putty_reg.mustache'  # TODO review default to Putty registry output
    in_filename_lower = in_filename.lower()
    in_filename_exten = os.path.splitext(in_filename_lower)[-1]

    input_format = options.input_format
    if not input_format:  # for now use as-is without validation
        if in_filename_lower.endswith('.tstk'):
            input_format = FORMAT_TSTK
        elif in_filename_lower.endswith('.reg'):
            input_format = FORMAT_PUTTY
        elif in_filename_lower.endswith('.itermcolors'):
            input_format = FORMAT_ITERM2
        elif in_filename_lower.endswith('.toml'):
            input_format = FORMAT_ALACRITTY_TOML
        elif in_filename_lower.endswith('.yaml'):  # See https://github.com/tinted-theming/schemes/tree/spec-0.11/base24
            input_format = FORMAT_BASE24
        # TODO determine format file contents (magic)

    if input_format == FORMAT_TSTK:
        f = open(in_filename, 'r')
        x = f.read()
        f.close()

        # FIXME assume tstk json input
        color_dict = json.loads(x)
    elif input_format == FORMAT_ITERM2:
        color_dict = iterm2_reader.read_and_convert_iterm(in_filename)
    elif input_format == FORMAT_ALACRITTY_TOML:
        color_dict = alacritty_reader.read_and_convert_alacritty_toml(in_filename)
    elif input_format == FORMAT_BASE24:
        color_dict = base24_reader.read_and_convert_base24_yaml(in_filename)
    elif input_format == FORMAT_PUTTY:
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
    elif input_format == FORMAT_PYWAL:
        color_dict = pywal_reader.read_and_convert_pywal(in_filename)
    else:
        raise NotImplementedError('Unknown input format %r (%r). Available %r' % (input_format or 'UKNOWN', in_filename_exten, ALL_FORMATS))

    template_dict = putty_colors_render_template.process_theme(color_dict, guess_theme_name=os.path.basename(in_filename))  # means sanity check will take place, before raw dump
    # TODO / FIXME slug-name URI escape processing
    if options.output_extension is not None:
        if not options.output:
            # default filename to something based on name in the theme and requested file extension
            options.output = template_dict['scheme-slug'] + options.output_extension  # or 'scheme-name'
            options.output = putty_colors_render_template.clean_filename(options.output)
    if not options.output:
        options.output = '-'  # default to stdout if no output specified
    if options.output != '-':
        #raise NotImplementedError('TODO non-stdout')
        f_out = open(options.output, 'w')
    else:
        f_out = sys.stdout
    if options.raw:
        # TODO not sure about writing text/strings to stdout...
        f_out.write('%s' % json.dumps(color_dict, indent=4))  # , sort_keys=True))  # sorting order is not natural :-(
        return 0


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

    if options.output != '-':
        print('Wrote to %s' % options.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
