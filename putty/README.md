
## Tools

  * batch_build.py - Batch render themes with any template
  * json2putty_reg.py - Render Putty registry file using a json file as input
      * putty_template.json - template json file ready to be filled in with decimal RGB values
  * putty_reg2json.py - Convert a Windows registry export of a single Putty session into a json (theme) to stdout - Clone of putty_reg_file_to_sorted.py (sans reg output) - todo refactor and share code
  * putty_reg_file_template.py - given a putty reg file, output a sorted, commented out reg file suitable for comparison/diff
  * putty_reg_file_to_sorted.py - takes in registry file (from a Putty session) prints sorted reg file to stdout (for easier diff-ing). optionally output json too
  * python_windows_registry_putty_colors.py - show Putty Windows Registry sessions that have identical color schemes (and write reg file to disk)

  * putty_colors_render_template.py - library for rendering base16 and terminal_style_toolkit - tinted theming templates

## Windows Registry Tips

### Export Unique Putty Sessions


Using python_windows_registry_putty_colors.py, NOTE output goes to directory `generated`.

    py -3 python_windows_registry_putty_colors.py


### Export All Putty Sessions

Using Windows registry tool.

    REM NOTE by default exports to directory C:\Windows\System32\
    regedit /e all_putty_sessions.reg HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\

    REM Export to current directory
    regedit /e %CD%\all_putty_sessions.reg HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\

## Render tools

Assuming there is a color scheme/theme file in json format with Putty colors in it, for example, TODO...


## Demo

### Export Putty all sessions into registry files

    py -3 python_windows_registry_putty_colors.py

### Convert a Putty registry files into json

Picking default reg file exported above `generated\DefaultPuttySettings_sorted.reg`

    py -3 putty_reg2json.py generated\DefaultPuttySettings_sorted.reg
    py -3 putty_reg2json.py generated\DefaultPuttySettings_sorted.reg > myfile.json

JSON file is all colors in decimal RGB format (just like Putty Registry settings).

### Convert a json (putty) file into Putty Windows Registry file

Assuming file from above:

    py -3 json2putty_reg.py myfile.json

Will generate UNKNOWN_sorted.reg with an unknown session name.

Passing in additional parameters, template and output filename will allow alternative output.
For example.

    py -3 json2putty_reg.py myfile.json colortable_html.mustache out.html

Will generate a html preview of the color theme.

THis can be used to preview what existing Putty sessions look like OR preview converted Gogh themes (see parent directory tool goghjson2puttyjson.py).
