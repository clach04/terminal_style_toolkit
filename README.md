# terminal_style_toolkit

Scripts / tools / config for terminal styling and colors / colours

- [terminal_style_toolkit](#terminal-style-toolkit)
  * [Notes](#notes)
    + [Fonts Notes](#fonts-notes)
  * [Sample files](#sample-files)
  * [Scripts for running in terminal](#scripts-for-running-in-terminal)
  * [Conversion tools](#conversion-tools)
  * [Misc tools](#misc-tools)
  * [Putty](#putty)
  * [Microsoft Windows CMD.exe](#microsoft-windows-cmdexe)
  * [Resources](#resources)
    + [Color Codes](#color-codes)
    + [Color Tools](#color-tools)
    + [vim](#vim)
    + [ls colors / dir_colors](#ls-colors---dir-colors)
    + [Related projects](#related-projects)
      - [Non-Terminal](#non-terminal)
    + [TODO Resources](#todo-resources)
      - [Color Scheme Collections](#color-scheme-collections)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Notes

When testing out a color scheme/theme consider different use cases:

  * `pyshow_colors2.py`
  * ls colors (LSCOLORS, LS_COLORS, `dircolors` and .dir_colors)
      * https://github.com/dracula/putty/issues/3
      * https://github.com/joshjon/bliss-dircolors - good starting point
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
      * FiraMono - https://mozilla.github.io/Fira/
      * Go-Mono
      * InconsolataGo https://github.com/im-AMS/Inconsolata-Nerd-Font-with-ligatures
      * Overpass
      * UbuntuMono
  * Fantasque Sans Mono - https://github.com/belluzj/fantasque-sans
  * Iosevka
      * http://be5invis.github.io/Iosevka
      * https://github.com/be5invis/Iosevka
      * https://typeof.net/Iosevka/


## Sample files

  * [sample_text_editor.txt](sample_text_editor.txt) utf-8 text file to test view/edit of fixed width fonts.
    Not suitable for in depth syntax highlighting tests.
  * https://github.com/altercation/solarized/tree/master/utils/tests has a collection of (small) different source code file types for testing syntax highlighting.
  * https://github.com/darekkay/config-files/tree/master/color-schemes/example-files

## Scripts for running in terminal

  * truecolor.awk modified from https://github.com/sonph/dotfiles/blob/master/bin/truecolor.sh - truecolor test
  * invaders.bash from https://paste.xinu.at/m-dAiJ/
  * show_colors.bash from https://bbs.archlinux.org/viewtopic.php?id=51818&p=1%29
      * Unknown license, many different versions of this script online
  * show_colors2.bash my version derived from show_colors.bash
  * color-test.bash - derived from https://gilesorr.com/bashprompt/howto/c333.html - shows all foreground colors as text with default background as a sanity check
  * pyshow_colors2.py in-progress Python version of show_colors2.bash
  * colors.py from https://gist.github.com/lilydjwg/fdeaf79e921c2f413f44b6f613f6ad53
  * parse_palette_tools.py - tools for dumping palettes for easier read/conversion

## Conversion tools

  * putty/any2theme.py - Convert many input theme formats and render with any template (or output raw tstk json). Input files supported; tstk json, Alacritty TOML, iTerm2, Putty reg, pywal16
  * parse_palette_tools.py - tools for dumping palettes for easier read/conversion
  * alacritty_yaml2toml.py - rough convert alacritty YAML into alacritty TOML
  * goghjson2puttyjson.py - tools for converting [Gogh JSON](https://github.com/Gogh-Co/Gogh/tree/master/json) Color Schemes from https://github.com/Gogh-Co/Gogh/ into json that Putty conversion tools (json2putty_reg.py) can use
  * pywaltemplate2puttymustache.py - convert pywal16 template
  * putty/json2putty_reg.py - convert (Putty) json into Putty registry import and html preview - Used to create https://github.com/clach04/putty_themes
  * Also see https://github.com/clach04/themer

## Misc tools

  * mintty_screenshot.py - launch mintty with specific theme and run pyshow_colors2 and then take a screenshot
    To setup: `pip install -r requirements_optional.txt`
    Screenshots are in BMP format, strongly recommend converting to PNG for size/space reasons.

## Putty

See [Putty tools readme](./putty/README.md) and also https://github.com/clach04/putty_themes/

  * python_windows_registry_putty_colors.py - dumps session names and colors (only)
    along with simple show sessions that use the exact same same-color scheme feature
  * Sane Putty settings https://web.archive.org/web/20191231204120/http://dag.wiee.rs/blog/content/improving-putty-settings-on-windows
    lots of good tips, identifies the problem with the out of box blue color in Putty, recommends:
    * ANSI Blue;        Red: 74 Green: 74   Blue:255
    * ANSI Blue Bold;   Red:140 Green:140   Blue:255
  * https://www.thegeekstuff.com/2009/07/10-practical-putty-tips-and-tricks-you-probably-didnt-know/

## Microsoft Windows CMD.exe

See Color Tool (ColorTool) https://github.com/microsoft/terminal/releases/tag/1904.29002
The `campbell.ini` color scheme is the Windows 10 Fall Creator's Update CMD out-of-box colors if need to restore to original colors.

From https://github.com/microsoft/terminal/tree/1904.29002/tools/ColorTool readme:
  * cmd-legacy is the legacy color scheme of the Windows Console, before July 2017
  * campbell is the new default scheme used by the Windows Console Host, as of the Fall Creator's Update.

NOTE latest ColorTool source is located in https://github.com/microsoft/terminal/tree/main/src/tools/ColorTool

ColorTool can use:

1. json format as used by concfg https://github.com/lukesampson/concfg
2. XML format as used by iTerm2-Color-Schemes - https://github.com/mbadolato/iTerm2-Color-Schemes/
3. INI format, as provided in samples for ColorTool https://github.com/microsoft/terminal/tree/main/src/tools/ColorTool

## Resources

### Color Codes

ANSI colors are often named:

    0    black
    1    dark red
    2    dark green
    3    brown
    4    dark blue
    5    dark magenta
    6    dark cyan

    7    light grey
    8    dark grey
    9    red
    10   green
    11   yellow
    12   blue
    13   magenta
    14   cyan
    15   white

  * https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit
  * https://github.com/termstandard/colors
  * https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences/75985833#75985833
    useful table of codes

### Color Tools

  * http://colorlab.wickline.org/colorblind/colorlab/ - view colors in web browser and simulate color blindness
  * https://terminal.sexy/
  * https://it-tools.tech/color-converter
      * https://github.com/CorentinTh/it-tools
  * https://iconscout.com/blog/best-color-palette-generators-for-any-design-project
  * https://colorffy.com/color-scheme-generator?color=257abb
  * https://github.com/clach04/themer
  * [pastel](https://github.com/sharkdp/pastel) A command-line tool to generate, analyze, convert and manipulate colors

### vim

  * https://bytefluent.com/vivify/ A ColorScheme Editor for Vim
  * https://github.com/chrisbra/Colorizer vim plugin to visualize hex color codes

vim themes that only use ANSI (16) colors - https://jeffkreeftmeijer.com/vim-16-color/
  * https://github.com/noahfrederick/vim-noctu
  * https://github.com/jeffkreeftmeijer/vim-dim/
  * https://github.com/dylanaraps/wal.vim - actually 8 colors
  * https://github.com/chriskempson/base16-vim/
  * NeoVim
      * https://github.com/uZer/pywal16.nvim
      * https://github.com/AlphaTechnolog/pywal.nvim
      * https://github.com/sonjiku/yawnc.nvim

### Midnight Commander

See https://github.com/jan-warchol/selenized/tree/putty/mc
and https://github.com/jan-warchol/selenized/issues/7

> MC's default color settings assume that terminal's blue will be very dark and suitable for use as background.

### ls colors / dir_colors

  * https://www.systutorials.com/docs/linux/man/5-dir_colors/
  * https://github.com/joshjon/bliss-dircolors
  * https://github.com/seebi/dircolors-solarized
  * https://github.com/nordtheme/dircolors
  * https://github.com/clach04?submit=Search&q=dircolors&tab=stars&type=&sort=&direction=&submit=Search
  * https://github.com/dracula/putty/issues/3 - Unreadable colors/colors with a=rwx permission directory and ls in color mode - default dircolors conflicts with terminal colors
  * Suggestion from https://github.com/jan-warchol/selenized/tree/putty/dircolors
    related to https://github.com/jan-warchol/selenized/issues/1

        # fix dircolors for Selenized
        export LS_COLORS="$LS_COLORS:ow=1;7;34:st=30;44:su=30;41"
  * https://github.com/sharkdp/vivid A themeable LS_COLORS generator with a rich filetype datebase

### Related projects

  * https://github.com/anonimoanemico/puttier
    * Supports previewing a theme
  * https://github.com/mvelikikh/putty-session-manager

#### Non-Terminal

  * https://github.com/monolifed/scite_theme scite themes from base16 config
  * https://github.com/mbadolato/iTerm2-Color-Schemes/tree/master/tools
  * https://github.com/Gogh-Co/Gogh/tree/master/tools
  * Base-16 and derivatives
  * https://github.com/worron/ACYLS - Any Color You Like Simple icon pack
  * Windows Color Pickers
      * http://instant-eyedropper.com/
          * https://github.com/miaupaw/instant-eyedropper
      * http://www.nattyware.com/pixie.php
      * https://colorcop.net/
          * https://github.com/ColorCop/ColorCop

### TODO Resources

  * https://blog.codinghorror.com/code-colorizing-and-readability/ note, cites studies with CRTs, pre lcd.

To checkout:

  * https://github.com/fikovnik/bin-scripts/blob/master/color-test.sh
  * https://github.com/fikovnik/bin-scripts/blob/master/term-colors.py
  * https://github.com/mvelikikh/putty-session-manager
  * https://ciembor.github.io/4bit/ - could code from https://github.com/ciembor/4bit be used as a web viewer preview (compare with puttier)

Color schemes that pass eyeball test but I'd like to checkout:

  * https://github.com/mattly/iterm-colors-farmhouse - light and dark
  * https://github.com/mattly/iterm-colors-pencil - light and dark
  * https://github.com/kepano/flexoki - light and dark

#### Color Scheme Collections

  * iTerm2
      * https://github.com/mbadolato/iTerm2-Color-Schemes - preview limited
          * https://iterm2colorschemes.com/
      * https://github.com/wozozo/Hemisu-Light-iTerm2
  * https://github.com/Gogh-Co/Gogh - OK preview, can at least see palette block to easily compare colors
      * https://gogh-co.github.io/Gogh/
      * 16 color themes that have bright/bold versions of base colors
          * Aci
          * Argonaut
          * Azu
          * Bim
          * Birds Of Paradise
          * Blazer
          * Blue Dolphin
          * ...
  * Alacritty
    * https://github.com/embark-theme/alacritty
    * https://github.com/rajasegar/alacritty-themes/ - no previews
      * https://github.com/rajasegar/alacritty-themes/blob/master/themes/IR-Black.toml
    * https://github.com/alacritty/alacritty-theme - preview limited
        * citylights
        * Cobalt2 - https://github.com/alacritty/alacritty-theme/blob/master/themes/Cobalt2.toml
        * dark_pastels
        * dark_plus
        * doom_one
        * dracula
        * dracula_plus
        * enfocado_dark
        * enfocado_light
        * flexoki
        * github_dark_high_contrast
        * github_light
        * google
        * gnome_terminal
        * gruvbox_dark
        * gruvbox_light
        * kanagawa_dragon
        * kanagawa_wave
        * midnight-haze
        * monokai
        * monokai_charcoal
        * monokai_pro
        * moonlight_ii_vscode
        * nord
        * oceanic_next
        * palenight
        * pencil_dark
        * pencil_light
        * remedy_dark
        * rose-pine
        * rose-pine-moon
        * smoooooth
        * synthwave_84
        * tango_dark
        * tomorrow_night_bright
        * wombat
        * zenburn
  * https://github.com/dylanaraps/paleta/tree/master/palettes
  * https://github.com/tinted-theming/home - technically tools and themes
      * https://github.com/tinted-theming/base16-putty
      * https://github.com/iamthad/base16-windows-command-prompt
      * https://github.com/InspectorMustache/base16-builder-python. - Todo my older version
  * Adwaita
      * https://en.wikipedia.org/wiki/Adwaita_(design_language)#Color
      * https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1.5/named-colors.html
  * pywal
      * https://github.com/embark-theme/pywal
          * https://embark-theme.github.io/#palette
  * vim
      * https://github.com/twerth/ir_black/
      * https://github.com/lifepillar/vim-wwdc16-theme/blob/master/colors/wwdc16.vim - note in Putty seems to work best when `:set t_Co=16`
