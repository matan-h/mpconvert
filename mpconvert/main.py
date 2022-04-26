import subprocess
import glob
import os
import pathlib
import traceback
from platform import system
from os import path as Path
import shutil
import sys
import PySimpleGUI as sg
# from .util import on_open, excepthook, popup_open_folder
from . import convert, errors
from .utils import location, guess_type
from typing import Sequence
from shutil import which
# convert.default_p = sg.popup_ok
sg.set_options(window_location=location or (None, None))
sg.theme('DarkAmber')  # Add a touch of color
sys.excepthook = errors.excepthook


def popup_open_folder(title, folder, file):
    """
    open popup window with title,for ask the user if want to open the file in Explorer,open file file with default application or not
    """
    if os.name == "nt":
        folder = str(pathlib.WindowsPath(folder))
        if file:
            file = str(pathlib.WindowsPath(file))
    startfile = os.__dict__.get(
        "startfile", lambda foldername: os.system('xdg-open "%s"' % foldername))

    layout = [
        [sg.T(title)],
        [sg.Ok(), sg.B(f"Open The {'File' if file else 'folder'} In Explorer", key="open-folder"),
         sg.B("Open the file (with default application)", key="open-file") if file else sg.T()]
    ]
    window = sg.Window(title, layout)
    event, values = window.read(close=True)
    if event == "open-folder":
        if file:
            print("open file in explorer:", file)
            # print("command:",f'start explorer /select,\"{file}\"')
            # explorer(file)
            if os.name == "nt":
                subprocess.call(["explorer", "/select", file], shell=True)
                # os.system(f'explorer /select,\"{file}\"')

            if system().lower() == "linux":
                app = None
                for fm in ["dolphin", "nautilus"]:
                    if shutil.which(fm) is not None:
                        app = fm
                        break
                if app:
                    subprocess.call([app, "--select", file])

        else:
            print("open folder in explorer:", folder)
            startfile(folder)
            # os.system(f'explorer \"{folder}\"')

    elif event == "open-file":
        if file:
            startfile(file)


def convert_safe(src: str, dst: str, _inp_type: str) -> int:
    """
    passed the arguments to convert.convert and if error occur write it to convert-error.txt

    Returns:1
    """
    try:
        # return convert.convert(src, dst, _inp_type)
        return convert.convertmap[_inp_type](src, dst)
    except Exception as _e:
        t = type(_e)

        convert_error_file = "convert-error.txt"
        print(str(_e), file=sys.stderr)
        importent = ''.join(map(lambda l: ']'.join(l.split("]")[
                            1:]), filter(lambda x: x.startswith('['), str(_e).split('\n'))))
        eh = str(_e).split("\n")[0]
        sg.popup_error(
            f"convert error:{eh}\nall traceback write to {convert_error_file}\n{importent}")
        with open(convert_error_file, "w") as convert_error_io:
            convert_error_io.write(traceback.format_exc())
        return 1  # error


#
def convert_multiple(files: Sequence[str], converts_folder: str, dst_file_extension: str, inp_type: str, messege: str, title: str) -> int:
    """
    open a progress bar to convert multiple files.

    Args:
        files: Sequence of files to convert
        converts_folder:the dst folder path
        dst_file_extension: the dst files extension
        inp_type:the type of convert
        messege:messege when done
        title: title of the progress bar

    Returns: 1 if error

    """
    sg.OneLineProgressMeter(title, 0, len(files), '-pb-')
    for file in files:
        if not sg.OneLineProgressMeter(title, files.index(file) + 1, len(files), '-pb-'):
            sg.OneLineProgressMeterCancel('-pb-')
            break
        dst_file = Path.join(converts_folder, Path.basename(
            Path.splitext(file)[0])) + "." + dst_file_extension if dst_file_extension else ''
        convert_exit_code = convert_safe(file, dst_file, inp_type)
        if convert_exit_code == 1:  # error
            sg.OneLineProgressMeterCancel('-pb-')
            return 1
    popup_open_folder(messege, converts_folder, None)


def main(file=None):
    """
    start gui.

    """
    if not file:
        popup_layout = [
            [sg.Text("please choose a file to convert")],
            [sg.Input(key="-file-"), sg.FileBrowse()],
            [sg.OK(key="-ok-"), sg.Cancel(key="-cancel-")]
        ]
        popup_win = sg.Window("Mpconvert", popup_layout)
        e, v = popup_win()
        popup_win.close()
        if e == "-cancel-" or not v["-file-"]:
            return 1  # exit,no file
        file = v["-file-"]

    if not os.path.exists(file):
        s = f'file not found:"{file}"'
        print(s)
        sg.popup(s)
        return 1

    #
    onlydir = Path.dirname(file)
    onlyname, file_extension = Path.splitext(file)
    # print("use name:", name)
    gs_type = guess_type(file)
    #
    # All the stuff inside your window.
    def title(_s, c=None): return sg.T(
        _s, font="Courier 40", text_color="#00cc00" if not c else c)
    # noinspection PyTypeChecker
    layout = [
        # ([sg.T(f"WARTING:{mess}", text_color="#ff0000")] if mess else []),
        [title("Info:", "#0099ff")],
        # [sg.Text('Use:', text_color="#0066ff"), sg.T(cls_vname, key="-use-", text_color="#0066ff")],
        [sg.Text('filename:', text_color="#0099ff"),
         sg.InputText(Path.basename(file), key="-file-", text_color="#0099ff")],
        [sg.T()],
        [title("Convert:")],
        [sg.T("Convert To:"), sg.InputText(Path.basename(onlyname), key="-convert-file-"), sg.T("with extension:"),
         sg.InputText("", size=(None, 40), key="-convert-file-extension-")],
        [sg.T("Convert as:"),
         sg.Combo(list(convert.convertmap.keys()), size=(None, 40), key='-inp-type-', default_value=gs_type,
                  enable_events=True)],
        [sg.B("Convert", button_color=(None, "#00cc00"), key="-convert-")],
        [sg.B(f"Convert all {file_extension} files in folder",
              button_color=(None, "#00cc00"), key="-convert-all-")],
    ]

    # Create the Window
    window = sg.Window('Convert Gui', layout, resizable=True).finalize()
    window.bring_to_front()
    # convert_object.gui_window = window
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window
            break

        elif event == "-resave-":
            to_file = Path.join(onlydir, values["-file-"])
            try:
                shutil.copy(file, to_file)
                print(f"done resave file {file} to file {to_file}")
            except Exception as e:
                print(e)

        elif event in ["-convert-", "-convert-all-"]:
            inp_type = window["-inp-type-"].Get()
            dst_file_extension: str = values["-convert-file-extension-"]
            dst_file_extension = dst_file_extension.strip()
            to_file = values['-convert-file-']
            if not to_file:
                sg.popup_error(
                    "you need to type a filename for convert", title="need to type filename")
                continue
            #
            dst_file = None
            if dst_file_extension:
                if dst_file_extension[0] == ".":
                    dst_file_extension = dst_file_extension[1:]

            if event == "-convert-":
                dst_file = Path.join(onlydir, to_file) + "." + \
                    dst_file_extension if dst_file_extension else ''
                n = convert_safe(file, dst_file, inp_type)
                if n == 1:  # error
                    continue

            elif event == "-convert-all-":
                converts_folder = Path.join(onlydir, "converts")
                if not Path.exists(converts_folder):
                    os.mkdir(converts_folder)
                glob_p = Path.join(onlydir, "*" + file_extension)
                print("glob search", glob_p)
                files_list = glob.glob(glob_p)
                if not files_list:
                    sg.popup("cant find files in this folder",
                             f"(with pattern:\"{glob_p}\")")
                    continue
                #
                convert_code = convert_multiple(files_list, converts_folder, dst_file_extension, inp_type,
                                                f'done convert all to foramat {dst_file_extension}', 'convert all')

                if convert_code == 1:  # error
                    continue
            if event == "-convert-":
                s = f"done convert '{to_file}' to format {dst_file_extension}"
                # ################################### both
                print(s)
                # sg.popup(s)
                if dst_file:
                    # noinspection PyTypeChecker
                    ex = Path.dirname(dst_file)
                else:
                    ex = None

                popup_open_folder(s, ex, dst_file)

    window.close()


def multiple(files: Sequence[str]):
    """
    multiple window convert window

    Args:
        files: Sequence of file to convert

    """
    try:
        gs_type = guess_type(files[0])
    except Exception:
        gs_type = None
    #
    onlydir = os.path.dirname(files[0])
    #
    layout = [
        [sg.T("Convert All selected files To:"), sg.InputText(
            "", size=(None, 40), key="-convert-file-extension-")],
        [sg.T("Convert All as:"),
         sg.Combo(list(convert.convertmap.keys()), size=(None, 40), key='-inp-type-', default_value=gs_type, )],
        [sg.B("Convert All", button_color=(None, "#00cc00"),
              key="-convert-", bind_return_key=True)],
    ]
    window = sg.Window('Convert Multiple files', layout).finalize()
    window.bring_to_front()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window
            break

        elif event == "-convert-":
            inp_type = values["-inp-type-"]
            dst_file_extension: str = values["-convert-file-extension-"].strip()
            #
            if dst_file_extension:
                if dst_file_extension[0] == ".":
                    dst_file_extension = dst_file_extension[1:]
            #
            converts_folder = Path.join(onlydir, "converts")
            if not Path.exists(converts_folder):
                os.mkdir(converts_folder)
            #
            convert_multiple(files, converts_folder, dst_file_extension, inp_type,
                             f"done convert selected files to format {dst_file_extension}", 'convert selected files')


if __name__ == '__main__':
    main()
