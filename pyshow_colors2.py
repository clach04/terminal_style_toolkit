#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Python version of show_colors2.bash - missing detected terminal features
NOTE expects terminal to be 86 characters wide
Shows:
  1. table of combinations of foreground and background colors
  2. block colors - not a feature in show_colors2.bash
  3. text colors - not a feature in show_colors2.bash
"""

import os
import sys

try:
    import colorama
    colorama.just_fix_windows_console()
except ImportError:
    if sys.platform.startswith('win'):
        print('Windows platform detected without colorama, refusing to run')
        sys.exit(0)


color_map_list_of_tuples_fg = [
    ('    m', 'normal'),
    ('   1m', 'bold'),
    ('  30m', 'black'),
    ('1;30m', 'blackB'),
    #('  90m', 'blackH'),
    ('  31m', 'red'),
    ('1;31m', 'redB'),
    #('  91m', 'redH'),
    ('  32m', 'green'),
    ('1;32m', 'greenB'),
    #('  92m', 'greenH'),
    ('  33m', 'yellow'),
    ('1;33m', 'yellowB'),
    #('  93m', 'yellowH'),
    ('  34m', 'blue'),
    ('1;34m', 'blueB'),
    #('  94m', 'blueH'),
    ('  35m', 'magenta'),
    ('1;35m', 'magentaB'),
    #('  95m', 'magentaH'),  # Bright / High
    ('  36m', 'cyan'),
    ('1;36m', 'cyanB'),
    #('  96m', 'cyanH'),
    ('  37m', 'white'),
    ('1;37m', 'whiteB'),
    #('  97m', 'whiteH'),
    #('  39m', 'Default'),  # TODO
    #('1;39m', 'DefaultB'),  # TODO
    #('  99m', 'DefaultH'),  # TODO
]
color_map_list_of_tuples_bg = [
    ('40m', 'black'),
    ('41m', 'red'),
    ('42m', 'green'),
    ('43m', 'yellow'),
    ('44m', 'blue'),
    ('45m', 'magenta'),
    ('46m', 'cyan'),
    ('47m', 'white'),
    #('100m', 'blackH'),
    #('101m', 'redH'),
    #('102m', 'greenH'),
    #('103m', 'yellowH'),
    #('104m', 'blueH'),
    #('105m', 'magentaH'),
    #('106m', 'cyanH'),
    #('107m', 'whiteH'),
    #('109m', 'DefaultH'),
]
color_map_list_of_tuples = color_map_list_of_tuples_fg + color_map_list_of_tuples_bg

color_map = dict(color_map_list_of_tuples)

foreground_colors = [x[0] for x in color_map_list_of_tuples_fg]
background_colors = [x[0] for x in color_map_list_of_tuples_bg]


f = sys.stdout
# heaeder

f.write('                      ')  # TODO replace with count
for bg in background_colors:
    f.write('%8s' %  color_map[bg])
f.write('\n')

"""
f.write('                         ')  # TODO replace with count
#f.write('                      ')  # TODO replace with count
for bg in background_colors:
    f.write('%-8s' %  bg)
f.write('\n')
"""
f.write('                         40m     41m     42m     43m     44m     45m     46m     47m\n')

# table

demo_text = 'gYw'   # The test text
for fg in foreground_colors:
    fgcolor_name = color_map[fg]
    f.write('%8s' %  fgcolor_name)  # 8 is the max string length of color_map values
    f.write(' %s' %  fg)  # already spaced/indented/justified
    fg = fg.strip()
    f.write('   \033[%s%s' % (fg, demo_text))  # already spaced/indented/justified
    f.write('  ')
    for bg in background_colors:
        f.write(' \033[%s\033[%s  %s  \033[0m' % (fg, bg, demo_text))
    f.write('\033[0m')  # reset - not needed but send just-in-case
    f.write('\n')

############
color_map_list_of_tuples_bg_rest = [
    ('100m', 'blackH'),
    ('101m', 'redH'),
    ('102m', 'greenH'),
    ('103m', 'yellowH'),
    ('104m', 'blueH'),
    ('105m', 'magentaH'),
    ('106m', 'cyanH'),
    ('107m', 'whiteH'),
    ('109m', 'DefaultH'),
]
demo_text = '   '
f.write('\n')
for bg_escape, bgcolor_name in color_map_list_of_tuples_bg:
    f.write('\033[%s%s' % (bg_escape, demo_text))
    f.write('\033[0m')  # reset - not needed but send just-in-case
f.write('\n')
for bg_escape, bgcolor_name in color_map_list_of_tuples_bg_rest:
    f.write('\033[%s%s' % (bg_escape, demo_text))
    f.write('\033[0m')  # reset - not needed but send just-in-case
f.write('\n')

f.write("\033[0mCOLOR_NC (No color)\n")
f.write("\033[1;37mCOLOR_WHITE\t\033[0;30mCOLOR_BLACK\n")
f.write("\033[0;34mCOLOR_BLUE\t\033[1;34mCOLOR_LIGHT_BLUE\n")
f.write("\033[0;32mCOLOR_GREEN\t\033[1;32mCOLOR_LIGHT_GREEN\n")
f.write("\033[0;36mCOLOR_CYAN\t\033[1;36mCOLOR_LIGHT_CYAN\n")
f.write("\033[0;31mCOLOR_RED\t\033[1;31mCOLOR_LIGHT_RED\n")
f.write("\033[0;35mCOLOR_PURPLE\t\033[1;35mCOLOR_LIGHT_PURPLE\n")
f.write("\033[0;33mCOLOR_YELLOW\t\033[1;33mCOLOR_LIGHT_YELLOW\n")
f.write("\033[1;30mCOLOR_GRAY\t\033[0;37mCOLOR_LIGHT_GRAY\n")
# reset
f.write("\033[0m")
