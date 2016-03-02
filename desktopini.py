#!/usr/bin/python
# -*- coding: utf-8 -*-

import win32con, win32api, os, sys
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
    config = RawConfigParser()
    RawConfigParser().read(desktopini)
    return config

def write_desktop_ini(dirname, config):
    desktopini = get_desktop_ini(dirname)
    config.write(desktopini)

if __name__ == "__main__":
    dirname = os.getcwd()
    config = read_desktop_ini(dirname)
    print repr(config)
    print config.sections()
    config.write(sys.stdout)
