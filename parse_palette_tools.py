#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import struct
import sys

def parse_adobe_act(filename):
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as file:
        if filesize == 772:  # CS2
            file.seek(768, 0)
            nbcolors = struct.unpack('>H', file.read(2))[0]
            file.seek(0, 0)
        else:
            nbcolors = filesize // 3

        # List of (R, G, B) tuples.
        return [struct.unpack('3B', file.read(3)) for i in range(nbcolors)]

def open_parse_gimp_palette_gpl_file(filename):
    f = open(filename)

    color_names = {}
    color_names_list = []  # ordered as found in GIMP Palette gpl file
    found_colors = False
    color_entry_style = 'UNKNOWN'
    for line in f:
        line = line.strip()
        if not line:
            continue
        #print('*LINE: %r' % line)
        if line == '#':
            found_colors = True
            continue
        if not found_colors and line.startswith('#Colors:'):
            color_entry_style = 'DECIMAL_RBG+HEX'
            found_colors = True
            continue
        if not found_colors and line.startswith('Name:'):
            continue
        if not found_colors and line.startswith('Columns:'):
            expected_column_count = int(line.split(':')[1])  # expecting 3....
            if expected_column_count == 3:
                color_entry_style = 'NAMED'  # 3 for RGB and + 1 for name
            else:
                raise NotImplementedError('%d columns for colors' % expected_column_count)
            continue
        if found_colors:
            #print('LINE: %r' % line)
            #print('LINE: %r' % line.split())
            if color_entry_style == 'NAMED':
                colors, color_name = line.split('\t')
                r, g, b = map(int, colors.split())
                #print(color_name, r, g, b)
                if color_name in color_names:
                    color_name += '_%02x%02x%02x' % (r, g, b)
                color_names[color_name] = (r, g, b)
            elif color_entry_style == 'DECIMAL_RBG+HEX':
                color_name = 'blank'
                r, g, b, hex_rgb = line.split('\t')
                colors = (r, g, b)
                r, g, b = map(int, colors)
                #print(color_name, r, g, b)
                if color_name in color_names:
                    color_name += '_%02x%02x%02x' % (r, g, b)
                color_names[color_name] = (r, g, b)
            else:
                raise NotImplementedError('Entry style %s' % color_entry_style)
            color_names_list.append(color_name)

    f.close()
    return color_names, color_names_list

argv = sys.argv
filename = argv[1]
color_names, color_names_list = open_parse_gimp_palette_gpl_file(filename)
for color_name in color_names:
    (r, g, b) = color_names[color_name]
    print('%02x%02x%02x\t%d,%d,%d\t%s' % (r, g, b, r, g, b, color_name, ))
    """
    print('%s' % color_name)
    print('%d,%d,%d' % (r, g, b))
    #print((r, g, b))
    print('%02x%02x%02x' % (r, g, b))
    print('')
    """

