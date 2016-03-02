#!/usr/bin/python
# -*- coding: utf-8 -*-

import win32con, win32api, os

def activate_desktop_ini(dirname):
    dektopini = os.path.join(dirname, "desktop.ini")
    with open(dektopini, 'a'):
        pass # just make sure desktop.ini already exists
    win32api.SetFileAttributes(dektopini, win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    win32api.SetFileAttributes(dirname, win32con.FILE_ATTRIBUTE_READONLY)

