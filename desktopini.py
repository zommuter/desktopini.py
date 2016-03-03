#!/usr/bin/python
# -*- coding: utf-8 -*-

import win32con, win32api, os, sys
from ctypes import byref, wintypes, create_unicode_buffer, windll
from ConfigParser import RawConfigParser, NoSectionError, NoOptionError

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
    with open(desktopini, 'r') as f:
        config.read(f)
    return config

def write_desktop_ini(dirname, config):
    desktopini = get_desktop_ini(dirname)
    with open(desktopini, 'w') as f:
        config.write(f)

def select_icon(iconpath=None, iconnum=0):
    if iconpath is None:
        iconpath = create_unicode_buffer(260)  # 260: https://stackoverflow.com/a/1880453/321973
    if iconnum == 0:
        iconnum = wintypes.INT(0)
    assert windll.shell32.PickIconDlg(None, byref(iconpath), len(iconpath), byref(iconnum)) == 1
    return iconpath.value, iconnum.value

if __name__ == "__main__":
    dirname = os.getcwd()
    config = read_desktop_ini(dirname)
    #config.add_section(".ShellClassInfo")
    try:
        iconpath, iconnum = config.get(".ShellClassInfo", "IconResource").split(",")
    except (NoSectionError, NoOptionError):
        iconpath, iconnum = create_unicode_buffer(260), wintypes.INT(0)
    print config.sections()
    config.write(sys.stdout)
    iconpath, iconnum =  select_icon(iconpath, iconnum)
    print "{},-{}".format(iconpath,iconnum)
    config.set(".ShellClassInfo", "IconResource", "{},-{}".format(iconpath,iconnum))
    config.write(sys.stdout)
    write_desktop_ini(dirname, config)
