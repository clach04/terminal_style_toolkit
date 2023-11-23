# Clone of putty_reg_file_json.py / putty_reg_file_to_sorted.py - todo refactor and share code
import json
import os
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


class UglyMustache:
    """Do not use this, it is ugly and extremely limited (...but doesn't need an external lib)
      * no white space support
      * no array support
      * no html support
      * no ... so much more stuff missing
    """
    def render(self, template_str, input_dict):
        for key in input_dict:
            template_str = template_str.replace('{{%s}}' % key, str(input_dict[key]))
        return template_str

filename = sys.argv[1]
strip_comments = True

filename = os.path.abspath(filename)
scheme_name = os.path.basename(filename)
scheme_name = scheme_name.split('.', 1)[0]
# FIXME clean filename some more
#print(scheme_name)
# Alternatively pick up scheme name from registry session name?


config_entry = []
for line in get_lines_from_file(filename, get_all_lines, mode='r'):
    if line.startswith('"'):
        config_entry.append(line)

#config_entry.sort()
config_entry = natural_sort(config_entry)

color_dict = {}
template_dict = {}
template_dict = {
    'scheme-name': scheme_name,
    'scheme-author': 'AUTHOR_HERE',
    'scheme-slug': scheme_name,
}
for line in config_entry:
    if not line.startswith('"Colour'):
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
    color_dict[color_number] = '%d,%d,%d' % (r, g, b)  # Decimal RGB, as used by Putty
    #color_dict[color_number] = '%02x%02x%02x' % (r, g, b)  # Hex RGB
    template_dict['%s-hex' % color_number] = '%02x%02x%02x' % (r, g, b)  # Hex RGB
    template_dict['%s-rgb-r' % color_number] = r
    template_dict['%s-rgb-g' % color_number] = g
    template_dict['%s-rgb-b' % color_number] = b

#print(';' * 65)
#print('')
#print('%s' % json.dumps(color_dict, indent=4))

# base16-like template (similar names for scheme, etc.)
template_str = """Windows Registry Editor Version 5.00

; Putty Theme {{scheme-name}}
; Scheme author: {{scheme-author}}
[HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\{{scheme-slug}}]

; Default Foreground
; Colour0 #{{Colour0-hex}}
"Colour0"="{{Colour0-rgb-r}},{{Colour0-rgb-g}},{{Colour0-rgb-b}}"

; Default Bold Foreground  -- equals to non-bold
; Colour1 #{{Colour1-hex}}
"Colour1"="{{Colour1-rgb-r}},{{Colour1-rgb-g}},{{Colour1-rgb-b}}"

; Default Background
; Colour2 #{{Colour2-hex}}
"Colour2"="{{Colour2-rgb-r}},{{Colour2-rgb-g}},{{Colour2-rgb-b}}"

; Default Bold Background  -- equals to non-bold
; Colour3 #{{Colour3-hex}}
"Colour3"="{{Colour3-rgb-r}},{{Colour3-rgb-g}},{{Colour3-rgb-b}}"

; Cursor Text -- equals to default background
; Colour4 #{{Colour4-hex}}
"Colour4"="{{Colour4-rgb-r}},{{Colour4-rgb-g}},{{Colour4-rgb-b}}"

; Cursor Colour -- equals to default foreground
; Colour5 #{{Colour5-hex}}
"Colour5"="{{Colour5-rgb-r}},{{Colour5-rgb-g}},{{Colour5-rgb-b}}"

; ANSI Black
; 30m
; Colour6 #{{Colour6-hex}}
"Colour6"="{{Colour6-rgb-r}},{{Colour6-rgb-g}},{{Colour6-rgb-b}}"

; ANSI Black Bright
; 1;30m
; Colour7 #{{Colour7-hex}}
"Colour7"="{{Colour7-rgb-r}},{{Colour7-rgb-g}},{{Colour7-rgb-b}}"

; ANSI Red
; 31m
; Colour8 #{{Colour8-hex}}
"Colour8"="{{Colour8-rgb-r}},{{Colour8-rgb-g}},{{Colour8-rgb-b}}"

; ANSI Red Bright
; 1;31m
; Colour9 #{{Colour9-hex}}
"Colour9"="{{Colour9-rgb-r}},{{Colour9-rgb-g}},{{Colour9-rgb-b}}"

; ANSI Green
; 32m
; Colour10 #{{Colour10-hex}}
"Colour10"="{{Colour10-rgb-r}},{{Colour10-rgb-g}},{{Colour10-rgb-b}}"

; ANSI Green Bright
; 1;32m
; Colour11 #{{Colour11-hex}}
"Colour11"="{{Colour11-rgb-r}},{{Colour11-rgb-g}},{{Colour11-rgb-b}}"

; ANSI Yellow
; 33m
; Colour12 #{{Colour12-hex}}
"Colour12"="{{Colour12-rgb-r}},{{Colour12-rgb-g}},{{Colour12-rgb-b}}"

; ANSI Yellow Bright
; 1;33m
; Colour13 #{{Colour13-hex}}
"Colour13"="{{Colour13-rgb-r}},{{Colour13-rgb-g}},{{Colour13-rgb-b}}"

; ANSI Blue
; 34m
; Colour14 #{{Colour14-hex}}
"Colour14"="{{Colour14-rgb-r}},{{Colour14-rgb-g}},{{Colour14-rgb-b}}"

; ANSI Blue Bright
; 1;34m
; Colour15 #{{Colour15-hex}}
"Colour15"="{{Colour15-rgb-r}},{{Colour15-rgb-g}},{{Colour15-rgb-b}}"

; ANSI Magenta
; 35m
; Colour16 #{{Colour16-hex}}
"Colour16"="{{Colour16-rgb-r}},{{Colour16-rgb-g}},{{Colour16-rgb-b}}"

; ANSI Magenta Bright
; 1;35m
; Colour17 #{{Colour17-hex}}
"Colour17"="{{Colour17-rgb-r}},{{Colour17-rgb-g}},{{Colour17-rgb-b}}"

; ANSI Cyan
; 36m
; Colour18 #{{Colour18-hex}}
"Colour18"="{{Colour18-rgb-r}},{{Colour18-rgb-g}},{{Colour18-rgb-b}}"

; ANSI Cyan Bright
; 1;36m
; Colour19 #{{Colour19-hex}}
"Colour19"="{{Colour19-rgb-r}},{{Colour19-rgb-g}},{{Colour19-rgb-b}}"

; ANSI White
; 37m
; Colour20 #{{Colour20-hex}}
"Colour20"="{{Colour20-rgb-r}},{{Colour20-rgb-g}},{{Colour20-rgb-b}}"

; ANSI White Bright
; 1;37m
; Colour21 {{Colour21-hex}}
"Colour21"="{{Colour21-rgb-r}},{{Colour21-rgb-g}},{{Colour21-rgb-b}}"
"""

#print('')
#print('')
stache = UglyMustache()
#print('%s' % UglyMustache.render(template_str, template_dict))  # classmethod
print('%s' % stache.render(template_str, template_dict))
