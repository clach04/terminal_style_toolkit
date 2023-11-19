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


config_entry = []
for line in get_lines_from_file(filename, get_all_lines, mode='r'):
    if not line.startswith('"'):
        print(line)
    else:
        config_entry.append(line)

#config_entry.sort()
config_entry = natural_sort(config_entry)

for line in config_entry:
    if not line.startswith('"Colour'):
        continue
    # NOTE assumes Color.... - no filtering..
    #print(line)
    shlex.shlex
    #print(shlex.split(line)[0].split('='))
    color_number, decimal_rgb = shlex.split(line)[0].split('=')
    #print(color_number, decimal_rgb)
    r, g, b = map(int, decimal_rgb.split(','))
    # print('%s %s %d,%d,%d #%02x %02x %02x ' % (color_number, decimal_rgb, r, g, b, r, g, b))
    print('; #%02x%02x%02x ' % (r, g, b))
    print(line)
