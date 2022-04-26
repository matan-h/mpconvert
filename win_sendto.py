import os
import shutil

import win32com.client
from os import path

Shell = win32com.client.Dispatch("Wscript.Shell")


def find_sendto():
    """
    find the "shell:sendto" folder

    Returns:the name of the sendto folder
    """
    sendto_folder = Shell.SpecialFolders("sendto")
    if not sendto_folder:
        sendto_folder = path.expandvars(r'%APPDATA%\Microsoft\Windows\SendTo')
    if not path.exists(sendto_folder):
        quit("sendto folder don't exists")
    return sendto_folder


def find_convert_path() -> str:
    """
    find the "shell:sendto" folder.

    Returns: sendto folder
    """
    convert_path = shutil.which('mpconvert.exe')  # if mpconvert is in %Path%
    if not convert_path:
        if path.exists(path.expandvars("%VIRTUAL_ENV%\\script\\mpconvert.exe")):
            convert_path = path.expandvars("%VIRTUAL_ENV%\\script\\mpconvert.exe")
    if not convert_path:
        print('cannot find mpconvert.exe script')

    if not os.path.isabs(convert_path):
        convert_path = os.path.abspath(convert_path)

    return convert_path


#
def CreateShortCut(lnk: str, target: str, working_in: str, args: str):  # ,icon
    """
    create link file.

    Args:
        lnk: path of file
        target: target of the link
        working_in: working directory of the link
        args: command-line args

    """
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
