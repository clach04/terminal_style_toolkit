# terminal_style_toolkit

Scripts / tools / config for terminal styling and colors / colours

## Notes

When testing out a color scheme/theme consider different use cases:

  * `pyshow_colors2.py`
  * ls colors (LSCOLORS, LS_COLORS, `dircolors` and .dir_colors)
      * https://github.com/dracula/putty/issues/3
  * neofetch
  * `vim` colorscheme

In general avoid:

  * Solutions that modify the TERM variable in .bashrc.
  * Solutions that modify the Vim t_Co variable.

### Fonts Notes

  * Under Linux, Bitstream Vera Sans Mono is typically built-in and not bad
  * Under Windows, the built-in Consolas is not bad (better than Courier New,
    that Putty defaults to), available since Microsoft Windows Vista.
    A similar (free) font is [Inconsolata](https://en.m.wikipedia.org/wiki/Inconsolata) / InconsolataGo (Inconsolata with straight quotes)
  * Many fonts at https://www.nerdfonts.com/ - worth checking out:
      * EnvyCodeR
      * FiraMono
      * Go-Mono
      * InconsolataGo https://github.com/im-AMS/Inconsolata-Nerd-Font-with-ligatures
      * Overpass
      * UbuntuMono

## Sample files

  * [sample_text_editor.txt](sample_text_editor.txt) utf-8 text file to test view/edit of fixed width fonts.
    Not suitable for in depth syntax highlighting tests.
  * https://github.com/altercation/solarized/tree/master/utils/tests has a collection of (small) different source code file types for testing syntax highlighting.
  * https://github.com/darekkay/config-files/tree/master/color-schemes/example-files

## Scripts for running in terminal

  * show_colors.bash from https://bbs.archlinux.org/viewtopic.php?id=51818&p=1%29
      * Unknown license, many different versions of this script online
  * show_colors2.bash my version derived from show_colors.bash
  * color-test.bash - derived from https://gilesorr.com/bashprompt/howto/c333.html - shows all foreground colors as text with default background as a sanity check
  * pyshow_colors2.py in-progress Python version of show_colors2.bash
  * colors.py from https://gist.github.com/lilydjwg/fdeaf79e921c2f413f44b6f613f6ad53
  * parse_palette_tools.py - tools for dumping palettes for easier read/conversion

## Putty

  * python_windows_registry_putty_colors.py - dumps session names and colors (only)
    along with simple show sessions that use the exact same same-color scheme feature
  * Sane Putty settings https://web.archive.org/web/20191231204120/http://dag.wiee.rs/blog/content/improving-putty-settings-on-windows
    lots of good tips, identifies the problem with the out of box blue color in Putty, recommends:
    * ANSI Blue;        Red: 74 Green: 74   Blue:255
    * ANSI Blue Bold;   Red:140 Green:140   Blue:255
  * https://www.thegeekstuff.com/2009/07/10-practical-putty-tips-and-tricks-you-probably-didnt-know/


## Resources

  * https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit
  * https://github.com/termstandard/colors
  * https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences/75985833#75985833
    useful table of codes

### Related projects

  * https://github.com/anonimoanemico/puttier
    * Supports previewing a theme
  * https://github.com/mvelikikh/putty-session-manager
  * https://github.com/mbadolato/iTerm2-Color-Schemes/tree/master/tools
  * https://github.com/Gogh-Co/Gogh/tree/master/tools
  * Base-16 and derivatives

#### Non-Terminal

  * https://github.com/monolifed/scite_theme scite themes from base16 config

### TODO Resources

To checkout:

  * https://github.com/fikovnik/bin-scripts/blob/master/color-test.sh
  * https://github.com/fikovnik/bin-scripts/blob/master/term-colors.py
  * https://github.com/mvelikikh/putty-session-manager
  * https://ciembor.github.io/4bit/ - could code from https://github.com/ciembor/4bit be used as a web viewer preview (compare with puttier)

Color schemes that pass eyeball test but I'd like to checkout:

  * https://github.com/mattly/iterm-colors-farmhouse - light and dark
  * https://github.com/mattly/iterm-colors-pencil - light and dark

#### Color Scheme Collections

  * https://github.com/mbadolato/iTerm2-Color-Schemes
  * https://github.com/Gogh-Co/Gogh
  * https://github.com/tinted-theming/home - technically tools and themes
