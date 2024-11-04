#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Batch process inputs to create theme.
"""

import glob
import os
import sys
import json

import putty_colors_render_template


directory_name = sys.argv[1]
try:
    template_filename = sys.argv[2]
except IndexError:
    template_filename = None
try:
    result_file_extension= sys.argv[3]
except IndexError:
    if template_filename:
        raise
    # default to Putty registry output
    result_file_extension= '.reg'
    template_filename = 'putty_reg.mustache'


for filename in glob.glob(os.path.join(directory_name, '*.tstk')):
    f = open(filename, 'r')
    x = f.read()
    f.close()


    theme_dict = json.loads(x)
    theme_dict['scheme-name'] = theme_dict.get('scheme-name') or 'UNKNOWN'
    session_name = theme_dict['scheme-name']
    file_name = theme_dict['scheme-slug'].replace('%20', ' ').replace(' ', '_')

    # FIXME detect missing colors
    reg_entries = putty_colors_render_template.render_template(theme_dict, template_filename)  # TODO see comment above, add sanity check parameter
    #out_filename = os.path.join(output_dir, session_name) + '_sorted.reg'
    #out_filename = session_name + result_file_extension
    out_filename = file_name + result_file_extension
    f = open(out_filename, 'w')
    f.write(reg_entries)
    f.close()
    print('Wrote to %s' % out_filename)
