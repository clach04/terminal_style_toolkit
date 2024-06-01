
## Tools

  * json2putty_reg.py - Render Putty registry file using a json file as input
      * putty_template.json - template json file ready to be filled in with decimal RGB values
  * putty_colors_render_template.py - library for rendering Putty colornames config giles into templates
  * putty_reg_file_json.py - Clone of putty_reg_file_to_sorted.py - todo refactor and share code
  * putty_reg_file_template.py - given a putty reg file, output a sorted, commented out reg file suitable for comparison/diff
  * putty_reg_file_to_sorted.py - takes in registry file (from a Putty session) prints sorted reg file to stdout (for easier diff-ing). optionally output json too
  * python_windows_registry_putty_colors.py - show Putty Windows Registry sessions that have identical color schemes (and write reg file to disk)

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

