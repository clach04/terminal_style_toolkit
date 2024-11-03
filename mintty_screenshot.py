#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Windows specific mintty launcher and screenshot taker

Usage note, move mouse pointer out of hte way (e.g. bottom right, left, etc.) this script will not move the mouse.

    (py3venv) C:\code\terminal\terminal_style_toolkit>type mintty_screenshot.minttyrc
    Font=Consolas
    FontHeight=10
    CursorType=block
    CursorBlinks=no

Also check contents of "%USERPROFILE%\.minttyrc" - recommend font/size along with Cursor setting (block, no flash/blink) for screenshot purposes

    C:\>type "%USERPROFILE%\.minttyrc"
    ThemeFile=rosipov
    Font=Consolas
    FontHeight=10
    CursorType=block
    CursorBlinks=no

What this tool does:

 1. Launch mintty
 2. Wait for it to load, then take a screenshot (BMP format)
 3. Wait for window to update (fixed sleep/pause time)
 4. Sends quit/exit event

Uses win32 API for grabbing bitmap, consider sending Alt+PrintScreen and grabbing from clipboard instead.
I've successfully used https://github.com/asweigart/pyautogui in the past for injecting key presses, not tried printscreen
see https://github.com/clach04/skipstone_server/blob/master/wdtv_sim.py
"""

import glob
import os
import subprocess
import sys
import time

import win32api  # sanity check, required by imports below. To install; py -3 -m pip install pywin32
import win32gui
import win32ui
import win32con


def take_screenshot(window_classname=None, window_title="mintty show colors", w=0, h=0, pause_time_in_seconds=0.5, bmp_filename_name="out.bmp"):
    """
    NOTE if window_classname / window_title are not set (and no window found, get black/empty bmp) so function will pause for pause_time_in_seconds and then try again
    set w/h if do not want original size
    """
    hwnd = win32gui.FindWindow(None, window_title)
    while not hwnd:
        print('Could not locate window titled, %r sleeping for %r seconds' %(window_title, pause_time_in_seconds))
        time.sleep(pause_time_in_seconds)
        hwnd = win32gui.FindWindow(None, window_title)

    time.sleep(pause_time_in_seconds)  # now sleep what we hope is long enough for window to be visible and updated with content

    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

    # Get the window rectangle
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    """
    print("Left:", left)
    print("Top:", top)
    print("Right:", right)
    print("Bottom:", bottom)
    print("across:", right - left)
    print("down:", bottom - top)
    """
    # NOTE the below ends up with a border (from desktop/windows underneath the window) :-(
    if not w:
        w = right - left
    if not h:
        h = bottom - top
    """
    print("across:", w)
    print("down:", h)
    """

    move_to_left = 0
    move_to_top = 0
    move_to_left = 800  # FIXME hard coded coordinates for my desktop so as to get white border around window..
    move_to_top = 90
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, move_to_left, move_to_top, w, h, 0)

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, bmp_filename_name)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.DeleteObject(dataBitMap.GetHandle())
    win32gui.ReleaseDC(hwnd, wDC)
    win32api.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)


def launch_mintty_and_screenshot(theme_name):
    # Currently theme_name is required, could be optional...

    mintty_title_text = "mintty show colors"
    mintty_title_text = "mintty theme: %s" % theme_name

    result = subprocess.run([
        r"C:\Program Files\Git\usr\bin\mintty.exe",
        "-c", "mintty_screenshot.minttyrc",
        "-o", "ThemeFile=%s" % theme_name,
        "--title", mintty_title_text,
        "--hold", "always",
        "--size", "90,65",  # number characters high, across
        "py", "-3", "pyshow_colors2.py", "show_cursor"  # command to run
    ])
    print('result %r' % result)  # can detect failure to launch mintty (catch FileNotFoundError:) BUT not python (at least with "--hold", "always")

    #take_screenshot(window_title=mintty_title_text)  # TODO slug filename, based on title/theme
    take_screenshot(window_title=mintty_title_text, bmp_filename_name=theme_name + '.bmp')

def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s\n\n' % (sys.version.replace('\n', ' - '), sys.platform))

    theme_name = "rosipov"
    themes_list = argv[1:]
    if not themes_list:
        themes_list = ["rosipov"]  # one of the defaults included/shipped with mintty
    if themes_list == ["all_user_themes"]:
        #themes_list = list(glob.glob(os.path.join(os.path.expanduser("~/mintty/themes"), '*')))
        themes_list = [os.path.basename(x) for x in
            glob.glob(os.path.join(os.environ["APPDATA"], "mintty", "themes", '*'))
        ]
    print(themes_list)
    for theme_name in themes_list:
        print(theme_name)
        launch_mintty_and_screenshot(theme_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())

