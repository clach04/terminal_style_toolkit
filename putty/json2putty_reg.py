#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Json to Windows registry session file for Putty

Expects json file to contain same values as Putty registry, i.e.:

    {
        "scheme-name" : "Optional name - can be omitted",
        "Colour0" : "187,187,187",
        ...
        "Colour21" : "238,238,236"
    }

Use putty_template.json as a starting point.
"""

import os
import sys
import json

import putty_colors_render_template


in_filename = sys.argv[1]  # json filename
try:
    template_filename = sys.argv[2]
except IndexError:
    template_filename = None
try:
    out_filename = sys.argv[3]
except IndexError:
    if template_filename:
        raise
    out_filename = None
f = open(in_filename, 'r')
x = f.read()
f.close()

template_filename = template_filename or 'putty_reg.mustache'  # default to Putty registry output

putty_color_dict = json.loads(x)
template_dict = putty_colors_render_template.process_theme(putty_color_dict)
"""
putty_color_dict['scheme-name'] = putty_color_dict.get('scheme-name') or 'UNKNOWN'
session_name = putty_color_dict['scheme-name']
file_name = putty_color_dict['scheme-slug'].replace('%20', ' ').replace(' ', '_')
"""
template_dict['scheme-name'] = template_dict.get('scheme-name') or 'UNKNOWN'
session_name = template_dict['scheme-name']
file_name = template_dict['scheme-slug'].replace('%20', ' ').replace(' ', '_')

# FIXME detect missing colors
#reg_entries = putty_colors_render_template.render_template(putty_color_dict, template_filename)  # TODO see comment above, add sanity check parameter
reg_entries = putty_colors_render_template.render_template(template_dict, template_filename, process_dict=False)  # TODO see comment above, add sanity check parameter
if not out_filename:
    #out_filename = os.path.join(output_dir, session_name) + '_sorted.reg'
    out_filename = file_name + '_sorted.reg'  # TODO slug or name?
f = open(out_filename, 'w')
f.write(reg_entries)
f.close()
print('Wrote to %s' % out_filename)
