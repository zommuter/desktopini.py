#!/usr/bin/python
# -*- coding: utf-8 -*-

import win32con, win32api, os, sys
from ctypes import byref, wintypes, create_unicode_buffer, windll
from ConfigParser import RawConfigParser, NoSectionError, NoOptionError


class DesktopIni(RawConfigParser):
    def __init__(self, dirname=None):
        #super(DesktopIni, self).__init__()  # ugh: https://stackoverflow.com/a/11527947/321973
        RawConfigParser.__init__(self)
        self.optionxform = str
        if dirname is None:
            dirname = os.getcwd()
        self.dirname = dirname
        self.desktopini = os.path.join(dirname, "desktop.ini")
        with open(self.desktopini, 'a') as f:  # make sure desktop.ini exists
            pass
        self.read(self.desktopini)

    def activate(self):
        win32api.SetFileAttributes(self.desktopini, win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
        win32api.SetFileAttributes(self.dirname, win32con.FILE_ATTRIBUTE_READONLY)

    def close(self):
        with open(self.desktopini, 'w') as f:
            self.write(f)


def select_icon(iconpath=None, iconnum=0):
    if iconpath is None:
        iconpath = create_unicode_buffer(260)  # 260: https://stackoverflow.com/a/1880453/321973
    if iconnum == 0:
        iconnum = wintypes.INT(0)
    assert windll.shell32.PickIconDlg(None, byref(iconpath), len(iconpath), byref(iconnum)) == 1
    return iconpath.value, iconnum.value

if __name__ == "__main__":
    desktopini = DesktopIni()
    desktopini.write(sys.stdout)
    if not desktopini.has_section(".ShellClassInfo"):
        desktopini.add_section(".ShellClassInfo")
    try:
        iconpath, iconnum = desktopini.get(".ShellClassInfo", "IconResource").split(",")
        iconpath = create_unicode_buffer(iconpath, 260)
        iconnum = wintypes.INT(-int(iconnum))
    except (NoSectionError, NoOptionError):
        iconpath, iconnum = create_unicode_buffer(260), wintypes.INT(0)
    print "{},-{}".format(iconpath.value,iconnum.value)
    iconpath, iconnum =  select_icon(iconpath, iconnum)
    print "{},-{}".format(iconpath,iconnum)
    desktopini.set(".ShellClassInfo", "IconResource", "{},-{}".format(iconpath,iconnum))
    desktopini.write(sys.stdout)
    desktopini.close()
