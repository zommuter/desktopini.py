#!/usr/bin/python
# -*- coding: utf-8 -*-

import win32con, win32api, os
from ConfigParser import RawConfigParser

def get_desktop_ini(dirname):
    desktopini = os.path.join(dirname, "desktop.ini")
    with open(desktopini, 'a'):
        pass # just make sure desktop.ini already exists
    return desktopini

def activate_desktop_ini(dirname):
    desktopini = get_desktop_ini(dirname)
    win32api.SetFileAttributes(desktopini, win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    win32api.SetFileAttributes(dirname, win32con.FILE_ATTRIBUTE_READONLY)

def read_desktop_ini(dirname):
    desktopini = get_desktop_ini(dirname)
    return RawConfigParser().read(desktopini)
