#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

# takes in registry file (from a Putty session) prints sorted reg file to stdout (for easier diff-ing). optionally output json too

import json
import re
import shlex
import sys

try:
    basestring
except NameError:
    try:
        basestring = (str, unicode)
    except NameError:
        basestring = str

import putty_colors_render_template

def get_all_lines(readobject):
    for line in readobject:
        line = line.strip()
        yield line

def get_lines_from_file(fileinfo, filer_iterator=None, mode='rb'):
    filer_iterator = filer_iterator or get_lines
    if isinstance(fileinfo, basestring):
        fileptr = open(fileinfo, mode)
    else:
        fileptr = fileinfo
    
    return filer_iterator(fileptr)

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)



filename = sys.argv[1]
try:
    template_filename = sys.argv[2]
except IndexError:
    template_filename = 'putty_reg.mustache'
strip_comments = True
dump_json = True
verbose = True

verbose = False
dump_json = False


config_entry = []
for line in get_lines_from_file(filename, get_all_lines, mode='r'):
    if not line.startswith('"'):
        if line.startswith(';'):
            #import pdb ; pdb.set_trace()
            if not strip_comments:
                # NOTE is do not strip comments, will be out of scope of original registry entry/setting
                # Also later strip any non-color entriees
                print(line)
        else:
            if verbose:
                print(line)
    else:
        config_entry.append(line)

#config_entry.sort()
config_entry = natural_sort(config_entry)

color_dict = {}
for line in config_entry:
    if not line.startswith('"Colour'):
        print('; IGNORED: %s' % line)  # TODO make this configurable?
        continue
    # NOTE assumes Color.... - no filtering..
    #print(line)
    shlex.shlex
    #print(shlex.split(line)[0].split('='))
    color_number, decimal_rgb = shlex.split(line)[0].split('=')
    #print(color_number, decimal_rgb)
    r, g, b = map(int, decimal_rgb.split(','))
    # print('%s %s %d,%d,%d #%02x %02x %02x ' % (color_number, decimal_rgb, r, g, b, r, g, b))
    if verbose:
        print('; #%02x%02x%02x ' % (r, g, b))
        print(line)
    color_dict[color_number] = '%d,%d,%d' % (r, g, b)  # Decimal RGB, as used by Putty
    #color_dict[color_number] = '%02x%02x%02x' % (r, g, b)  # Hex RGB

if dump_json:
    print(';' * 65)
    print('')
    print('%s' % json.dumps(color_dict, indent=4))

if verbose:
    print('')
    print('-' * 65)

reg_entries = putty_colors_render_template.render_template(color_dict, template_filename=template_filename)
print('%s' % reg_entries)
