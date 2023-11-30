import errno
import json
try:
    import winreg
except ImportError:
    import _winreg as winreg


try:
    FileNotFoundError
except NameError:
    # py2
    FileNotFoundError = OSError  # FIXME review, use variable for tuple of exceptions instead?

access_type = winreg.KEY_ALL_ACCESS  # needs admin, or get; WindowsError: [Error 5] Access is denied / PermissionError: [WinError 5] Access is denied 
access_type = winreg.KEY_READ 


key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\SimonTatham\\PuTTY\\Sessions\\", 0, access_type)
sessions = {}
colors_to_session_names = {}
for i in range(0, winreg.QueryInfoKey(key)[0]):
    putty_session_name = winreg.EnumKey(key, i)  # putty session name
    print('\t' + putty_session_name)
    skey = winreg.OpenKey(key, putty_session_name)
    try:
        """
        try:
            key_name = 'ANSIColour'
            print('\t\t' + key_name + ' ' , winreg.QueryValueEx(skey, key_name)[0])
        except (OSError, FileNotFoundError) as e:
            if e.errno == errno.ENOENT:
                # DisplayName doesn't exist in this skey
                pass
        try:
            key_name = 'BoldAsColour'  # a handful of my sessions have different values for this
            print('\t\t' + key_name + ' ' , winreg.QueryValueEx(skey, key_name)[0])
        except (OSError, FileNotFoundError) as e:
            if e.errno == errno.ENOENT:
                # DisplayName doesn't exist in this skey
                pass
        try:
            key_name = 'UseSystemColours'
            print('\t\t' + key_name + ' ' , winreg.QueryValueEx(skey, key_name)[0])
        except (OSError, FileNotFoundError) as e:
            if e.errno == errno.ENOENT:
                # DisplayName doesn't exist in this skey
                pass
        try:
            key_name = 'Xterm256Colour'
            print('\t\t' + key_name + ' ' , winreg.QueryValueEx(skey, key_name)[0])
        except (OSError, FileNotFoundError) as e:
            if e.errno == errno.ENOENT:
                # DisplayName doesn't exist in this skey
                pass
        """
        colors = {}
        for j in range(21+1):
            try:
                key_name = 'Colour%d' % j
                colors[key_name] = winreg.QueryValueEx(skey, key_name)[0]
                print('\t\t' + key_name + ' ' + winreg.QueryValueEx(skey, key_name)[0])
            except (OSError, FileNotFoundError) as e:
                if e.errno == errno.ENOENT:
                    # DisplayName doesn't exist in this skey
                    pass
        sessions[putty_session_name] = colors
        color_key = json.dumps(colors)
        tmp_list = colors_to_session_names.get(color_key, [])
        tmp_list.append(putty_session_name)
        colors_to_session_names[color_key] = tmp_list
    finally:
        skey.Close()

# show sessions that have identical color schemes
print('-' * 65)
print('sessions that have identical color schemes')
for x in colors_to_session_names:
    print(colors_to_session_names[x])
    print('\t%s' % x)
# Showing similar would require diffing each scheme and having a thresh hold for differences in color / and/or levingstien distance (etc.) for fuzzy match
print('-' * 65)
