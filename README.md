# terminal_style_toolkit

Scripts / tools / config for terminal styling and colors / colours

## Notes

When testing out a color scheme/theme consider different use cases:

  * `pyshow_colors2.py`
  * ls colors (LSCOLORS, LS_COLORS, `dircolors` and .dir_colors)
  * neofetch
  * `vim` colorscheme

In general avoid:

  * Solutions that modify the TERM variable in .bashrc.
  * Solutions that modify the Vim t_Co variable.

### Fonts Notes

  * Under Windows, the built-in Consolas is not bad (better than Courier New,
    that Putty defaults to), available since Microsoft Windows Vista.
    A similar (free) font is Inconsolata
  * Many fonts at https://www.nerdfonts.com/ - worth checking out:
      * EnvyCodeR
      * FiraMono
      * Go-Mono
      * InconsolataGo
      * Overpass
      * UbuntuMono

## Sample files

  * sample_text_editor.txt utf-8 text file to test view/edit of fixed width fonts.
    Not suitable for syntax highlighting tests.

## Scripts for running in terminal

  * show_colors.bash from https://bbs.archlinux.org/viewtopic.php?id=51818&p=1%29
      * Unknown license, many different versions of this script online
  * show_colors2.bash my version derived from show_colors.bash
  * pyshow_colors2.py in-progress Python version of show_colors2.bash
  * colors.py from https://gist.github.com/lilydjwg/fdeaf79e921c2f413f44b6f613f6ad53

## Putty

  * python_windows_registry_putty_colors.py - dumps session names and colors (only)
    along with simple show sessions that use the exact same same-color scheme feature
  * Sane Putty settings https://web.archive.org/web/20191231204120/http://dag.wiee.rs/blog/content/improving-putty-settings-on-windows
    lots of good tips, but it identifies the problem with the out of box blue color in Putty


## Resources

  * https://github.com/termstandard/colors
  * https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences/75985833#75985833
    useful table of codes

### TODO Resources

To checkout:

  * https://github.com/fikovnik/bin-scripts/blob/master/color-test.sh
  * https://github.com/fikovnik/bin-scripts/blob/master/term-colors.py
