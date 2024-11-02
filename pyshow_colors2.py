#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
r"""Python version of show_colors2.bash - missing detected terminal features
NOTE expects terminal to be 86 characters wide
Shows:
  1. table of combinations of foreground and background colors
  2. block colors - not a feature in show_colors2.bash
  3. text colors - not a feature in show_colors2.bash

Sample usage with mintty under Windows:

    "C:\Program Files\Git\usr\bin\mintty.exe" --title "mintty show colors" --hold  always --size 90,40 py -3 pyshow_colors2.py
    "C:\Program Files\Git\usr\bin\mintty.exe" --title "mintty show colors" --hold  always --size 90,50 py -3 pyshow_colors2.py
    "C:\Program Files\Git\usr\bin\mintty.exe" --title "mintty show colors" --hold  always --size 90,65 py -3 pyshow_colors2.py

"""

import os
import sys

is_win = sys.platform.startswith('win')

try:
    import colorama
    colorama.just_fix_windows_console()
except ImportError:
    if not os.environ.get('SKIP_WIN_CHECK'):
        if is_win and not ('TERM' in os.environ or 'TERM_PROGRAM' in os.environ):
            print('Windows platform detected without Colorama installed, refusing to run; SET SKIP_WIN_CHECK=true')
            print('    python -m pip install colorama')
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

reset = '\033[0m'
bold = '\033[1m'


def show_color_table_grid(f=sys.stdout):
    # header
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
        f.write(reset)  # reset - not needed but send just-in-case
        f.write('\n')


############


def show_color_block_table(f=sys.stdout, demo_text='   '):
    # TODO more options about table dimensions
    f.write('\n')
    for bg_escape, bgcolor_name in color_map_list_of_tuples_bg:
        f.write('\033[%s%s' % (bg_escape, demo_text))
        f.write(reset)  # reset - not needed but send just-in-case
    f.write('\n')
    for bg_escape, bgcolor_name in color_map_list_of_tuples_bg_rest:
        f.write('\033[%s%s' % (bg_escape, demo_text))
        f.write(reset)  # reset - not needed but send just-in-case
    f.write('\n')



def show_panels(f=sys.stdout):
    "foreground"
    # TODO background example as well, some modern terminals use different actual colors for fg/bg for same name/escape
    # TODO have one panel and generate on the fly, looping through colors. Be easier to have both fg and bg versions

    """
    for bg in background_colors:
        #f.write('%-7s' %  color_map[bg])
        f.write('%7s' %  color_map[bg])
    """
    #f.write(' black  red    green  yellow blue  magenta cyan   white')
    #f.write(' black    red  green yellow  blue magenta   cyan  white')
    f.write(' black    red  green yellow  blue  magenta  cyan  white')

    panels = """
 ${f0}████${b}▄${r}  ${f1}████${b}▄${r}  ${f2}████${b}▄${r}  ${f3}████${b}▄${r}  ${f4}████${b}▄${r}  ${f5}████${b}▄${r}  ${f6}████${b}▄${r}  ${f7}████${b}▄${r}
 ${f0}████${b}█${r}  ${f1}████${b}█${r}  ${f2}████${b}█${r}  ${f3}████${b}█${r}  ${f4}████${b}█${r}  ${f5}████${b}█${r}  ${f6}████${b}█${r}  ${f7}████${b}█${r}
 ${f0}████${b}█${r}  ${f1}████${b}█${r}  ${f2}████${b}█${r}  ${f3}████${b}█${r}  ${f4}████${b}█${r}  ${f5}████${b}█${r}  ${f6}████${b}█${r}  ${f7}████${b}█${r}
 ${b}${f0} ▀▀▀▀  ${b}${f1} ▀▀▀▀   ${f2}▀▀▀▀   ${f3}▀▀▀▀   ${f4}▀▀▀▀   ${f5}▀▀▀▀   ${f6}▀▀▀▀   ${f7}▀▀▀▀${r}
""".replace('${b}', bold).replace('${r}', reset)
    bg_panels = panels
    fg_panels = panels
    for x in range(8):
        bg_panels = bg_panels.replace('${f%d}' % x, '\033[4%dm' % x)  # FIXME "bold" optimization does NOT work for bg_bold, need entire escape sequence for each color in bold
        fg_panels = fg_panels.replace('${f%d}' % x, '\033[3%dm' % x)
    f.write(fg_panels)
    #f.write(bg_panels)  # TODO, see FIXME above and TODO at start of function



def show_descriptive_text_example(f=sys.stdout):
    f.write("\033[0mCOLOR_NC (No color)\n")
    f.write("\033[1;37mCOLOR_WHITE\t\033[0;30mCOLOR_BLACK\n")
    f.write("\033[0;34mCOLOR_BLUE\t\033[1;34mCOLOR_LIGHT_BLUE\n")
    f.write("\033[0;32mCOLOR_GREEN\t\033[1;32mCOLOR_LIGHT_GREEN\n")
    f.write("\033[0;36mCOLOR_CYAN\t\033[1;36mCOLOR_LIGHT_CYAN\n")
    f.write("\033[0;31mCOLOR_RED\t\033[1;31mCOLOR_LIGHT_RED\n")
    f.write("\033[0;35mCOLOR_PURPLE\t\033[1;35mCOLOR_LIGHT_PURPLE\n")
    f.write("\033[0;33mCOLOR_YELLOW\t\033[1;33mCOLOR_LIGHT_YELLOW\n")
    f.write("\033[1;30mCOLOR_GRAY\t\033[0;37mCOLOR_LIGHT_GRAY\n")
    f.write(reset)
    # TODO newline?


def show_raw_ansi_file(f=sys.stdout, num_cols=1, raw_ansi_filename='ls_colors_test.txt', description='$ ls --color=always test-dircolors/\n'):
    """
    Example:
        script ls_colors_test.txt
        ls --color=always test-dircolors/
        exit
        # then edit ls_colors_test.txt, top and tail it
    """
    if not os.path.exists(raw_ansi_filename):
        f.write('Missing %s ansi raw file' % raw_ansi_filename)
        return
    f_in = open(raw_ansi_filename)
    f.write(description)
    line_counter = 0
    for line in f_in:
        line_counter += 1
        if line_counter % num_cols:
            #line = line.replace('\n', '')
            line = line.strip()
            # TODO column line up...
            #line = line.replace('\n', '    ')  # TODO column line up...
            line = '%s  ' % line
            #line = '%-30s ' % line  # length specifier includes the ANSI escape sequence so alignment will be off :-(
            ##line = '%-30s \n%r\n' % (line, line)  # length specifier includes the ANSI escape sequence so alignment will be off :-(
        f.write(line)

def show_cursor(f=sys.stdout):
    f.write("$ ")
    _ = input('')


def main(argv=None):
    argv = argv or sys.argv
    #print('Python %s on %s' % (sys.version, sys.platform))

    f = sys.stdout

    # TODO add options to skip (via environment variables) some output
    show_color_table_grid(f)

    show_color_block_table(f)
    f.write('\n')

    show_panels(f)
    f.write('\n')

    show_descriptive_text_example(f)
    f.write('\n')

    show_raw_ansi_file(f)

    show_cursor(f)  # TODO command line flag/argument or environment variable to control this - mostly useful for mintty

    return 0

if __name__ == "__main__":
    sys.exit(main())
