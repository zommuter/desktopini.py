#!/usr/bin/python
# -*- coding: utf-8 -*-

import win32con, win32api, os, sys
from ctypes import byref, wintypes, create_unicode_buffer, windll
from configparser import RawConfigParser, NoSectionError, NoOptionError


class DesktopIni(RawConfigParser, object):
    def __init__(self, dirname=None):
        super(DesktopIni, self).__init__()
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
        windll.shell32.SHChangeNotify

    def deactivate(self):
        win32api.SetFileAttributes(self.desktopini, win32con.FILE_ATTRIBUTE_NORMAL)
        dirattr = win32api.GetFileAttributes(self.dirname) ^ win32con.FILE_ATTRIBUTE_READONLY
        win32api.SetFileAttributes(self.dirname, dirattr)

    def cleanup(self):
        for section in self.sections():
            if len(self.options(section)) == 0:
                self.remove_section(section)

    def close(self):
        self.cleanup()
        self.deactivate()
        if len(self.sections()) > 0:
            with open(self.desktopini, 'w') as f:
                self.write(f)
            self.activate()
        else:
            os.remove(self.desktopini)


class NoIconPickedError(Exception):
    pass

def select_icon(iconpath=None, iconnum=0):
    if iconpath is None:
        piconpath = create_unicode_buffer(260)  # 260: https://stackoverflow.com/a/1880453/321973
    else:
        piconpath = create_unicode_buffer(iconpath, 260)
    piconnum = wintypes.INT(iconnum)
    if windll.shell32.PickIconDlg(None, byref(piconpath), len(piconpath), byref(piconnum)) == 1:
        return piconpath.value, piconnum.value
    else:
        raise NoIconPickedError


if __name__ == "__main__":
    desktopini = DesktopIni()
    desktopini.write(sys.stdout)
    if not desktopini.has_section(".ShellClassInfo"):
        desktopini.add_section(".ShellClassInfo")
    try:
        iconpath, iconnum = desktopini.get(".ShellClassInfo", "IconResource").split(",")
        iconnum = -int(iconnum)
    except (NoSectionError, NoOptionError):
        iconpath, iconnum = "", 0
    print("{},{}".format(iconpath,iconnum))

    result = win32api.MessageBox(None, "Click no to remove setting, abort to keep previous setting.", "Customize icon?", win32con.MB_YESNOCANCEL)
    print(result)
    if result == win32con.IDYES:
        try:
            iconpath, iconnum =  select_icon(iconpath, iconnum)
        except NoIconPickedError:
            exit(19)
        desktopini.set(".ShellClassInfo", "IconResource", "{},{}".format(iconpath,iconnum))
        print("{},{}".format(iconpath,iconnum))
    elif result == win32con.IDNO:
        desktopini.remove_option(".ShellClassInfo", "IconResource")
    else:
        assert result == win32con.IDCANCEL

    desktopini.write(sys.stdout)
    desktopini.close()
