#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Dirty, minimal hack to convert alacritty yaml into toml (like) good enough to be readable
No actual yaml processing
Attempt to preserve comments
Ignore sections tstk has no suport for
"""

import glob
import os
import sys


is_win = sys.platform.startswith('win')


mapping = {
    'colors:': '',
    'primary:': '[colors.primary]',
    'cursor:': '[colors.cursor]',
    'selection:': '[colors.selection]',
    'normal:': '[colors.normal]',
    'bright:': '[colors.bright]',
}


def do_many_to_new_files(argv):
    if is_win:
        filenames = []
        for filename_pattern in argv[1:]:
            filenames += glob.glob(filename_pattern)
    else:
        filenames = argv[1:]
    print('%d files to convert' % len(filenames))
    #print(filenames)
    for theme_filename in filenames:
        print('... %s ... ' % (theme_filename, ))
        f = open(theme_filename)  # just assume this will work, correct text mode and encoding - assume utf-8

        toml_lines = []
        # TODO refactor into list append and return list...
        for line in f:
            line = line.strip()
            if line in mapping:
                line = line.replace(line, mapping[line])
            line = line.replace(':', '=')
            toml_lines.append('%s' % line)
        f.close()

        f = open(theme_filename + '.toml', 'w')  # just assume this will work, correct text mode and encoding - assume utf-8
        f.write('\n'.join(toml_lines))
        f.close()


def do_one_to_stdout(theme_filename):
    f = open(theme_filename)  # just assume this will work, correct text mode and encoding - assume utf-8

    # TODO refactor into list append and return list...
    for line in f:
        line = line.strip()
        if line in mapping:
            line = line.replace(line, mapping[line])
        line = line.replace(':', '=')
        print('%s' % line)

    f.close()


def main(argv=None):
    argv = argv or sys.argv
    #print('Python %s on %s' % (sys.version, sys.platform))

    #theme_filename = argv[1]
    #do_one_to_stdout(theme_filename)

    do_many_to_new_files(argv)

    return 0

if __name__ == "__main__":
    sys.exit(main())
