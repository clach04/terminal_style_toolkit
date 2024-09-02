#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Convert a Windows registry export of a single Putty session into a json (theme) file

Expects single byte or utf-8 encoded file, for example, UCS2/UTF-16 is NOT supported
"""

# Clone of putty_reg_file_to_sorted.py - todo refactor and share code
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
strip_comments = True


config_entry = []
# Simplistic registry file reader, assumes single byte or utf8 (i.e. not UCS2/UTF-16)
# Ignores key names, only looks at values
for line in get_lines_from_file(filename, get_all_lines, mode='r'):
    if line.startswith('"') or line.startswith('['):
        config_entry.append(line)

#config_entry.sort()
config_entry = natural_sort(config_entry)

template_dict = {}
template_dict = {
    'scheme-name': 'NAME_HERE',
    'scheme-author': 'AUTHOR_HERE',
    'scheme-slug': 'SLUG_HERE',
}

include_optional_values = False
include_optional_values = True

for line in config_entry:
    if line.startswith('[HKEY_CURRENT_USER\\Software\\SimonTatham\\PuTTY\\Sessions\\'):
        #print('GOT %r' % line)
        putty_session_name = line.rsplit('\\', 1)[-1]
        putty_session_name = putty_session_name[:-1]
        #print('GOT %r' % putty_session_name)
        template_dict['scheme-slug'] = template_dict['scheme-name'] = putty_session_name
        continue
    elif not line.startswith('"Colour'):
        #print('; IGNORED: %s' % line)  # TODO make this configurable?
        continue
    # NOTE assumes Color.... - no filtering..
    #print(line)
    shlex.shlex
    #print(shlex.split(line)[0].split('='))
    color_number, decimal_rgb = shlex.split(line)[0].split('=')
    #print(color_number, decimal_rgb)
    r, g, b = map(int, decimal_rgb.split(','))
    # print('%s %s %d,%d,%d #%02x %02x %02x ' % (color_number, decimal_rgb, r, g, b, r, g, b))
    #print('; #%02x%02x%02x ' % (r, g, b))
    #print(line)
    template_dict[color_number] = '%d,%d,%d' % (r, g, b)  # Decimal RGB, as used by Putty
    # Optional
    if include_optional_values:
        template_dict['%s-hex' % color_number] = '%02x%02x%02x' % (r, g, b)  # Hex RGB
        template_dict['%s-rgb-r' % color_number] = r
        template_dict['%s-rgb-g' % color_number] = g
        template_dict['%s-rgb-b' % color_number] = b

#print(';' * 65)
#print('')
# Dump json to stdout
print('%s' % json.dumps(template_dict, indent=4))
