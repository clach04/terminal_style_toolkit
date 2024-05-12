
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

Use putty_tempate.json as a starting point.
"""

import os
import sys
import json

import putty_colors_render_template


in_filename = sys.argv[1]
f = open(in_filename, 'r')
x = f.read()
f.close()

putty_color_dict = json.loads(x)
putty_color_dict['scheme-name'] = putty_color_dict.get('scheme-name', 'UNKNOWN')
session_name = putty_color_dict['scheme-name']

reg_entries = putty_colors_render_template.render_template(putty_color_dict)
#filename = os.path.join(output_dir, session_name) + '_sorted.reg'
filename = session_name + '_sorted.reg'
f = open(filename, 'w')
f.write(reg_entries)
f.close()
print('Wrote to %s' % filename)
