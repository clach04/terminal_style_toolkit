
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


in_filename = sys.argv[1]
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
putty_color_dict['scheme-name'] = putty_color_dict.get('scheme-name', 'UNKNOWN')
session_name = putty_color_dict['scheme-name']

# FIXME detect missing colors
reg_entries = putty_colors_render_template.render_template(putty_color_dict, template_filename)  # TODO see comment above, add sanity check parameter
if not out_filename:
    #out_filename = os.path.join(output_dir, session_name) + '_sorted.reg'
    out_filename = session_name + '_sorted.reg'
f = open(out_filename, 'w')
f.write(reg_entries)
f.close()
print('Wrote to %s' % out_filename)
