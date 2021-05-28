import os
import shutil

import win32com.client
from os import path

Shell = win32com.client.Dispatch("Wscript.Shell")


def find_sendto():
    sendto_folder = Shell.SpecialFolders("sendto")
    if not sendto_folder:
        sendto_folder = path.expandvars(r'%APPDATA%\Microsoft\Windows\SendTo')
    if not sendto_folder:
        quit('cannot find sendto folder')
    return sendto_folder


def find_convert_path():
    convert_path = shutil.which('mpconvert')

    if not convert_path:
        if path.exists(path.expandvars("%VIRTUAL_ENV%\\script\\mpconvert.exe")):
            convert_path = path.exists(path.expandvars("%VIRTUAL_ENV%\\script\\mpconvert.exe"))
    if not convert_path:
        print('cannot find mpconvert.exe script')
    return convert_path


#
def CreateShortCut(lnk, target, working_in, args):  # ,icon
    shortcut = Shell.CreateShortCut(lnk)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = working_in
    shortcut.Arguments = args
    shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
    # shortcut.IconLocation = icon
    shortcut.save()


if __name__ == '__main__':
    sendto = find_sendto()
    convert_path = find_convert_path()
    lnk = os.path.join(sendto, 'convert.lnk')
    CreateShortCut(lnk, convert_path, os.getcwd(), "/$MULTIPLE")
    print('shortcut created in \"%s\"' % lnk)
