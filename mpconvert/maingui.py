import glob
import os
import pathlib
import traceback
from os import path as Path
import shutil
import sys
import PySimpleGUI as sg
from . import info
from .util import on_open, excepthook, popup_open_folder, progress_bar
from . import convert

convert.default_p = sg.popup_ok


def convert_safe(src, dst, _inp_type):
    try:
        return convert.convert(src, dst, _inp_type)
    except Exception as _e:
        convert_error_file = "convert-error.txt"
        print(str(_e), file=sys.stderr)
        eh = str(_e).split("\n")[0]
        sg.popup_error(f"convert error:{eh}\nall traceback write to {convert_error_file}")
        with open(convert_error_file, "w") as convert_error_io:
            convert_error_io.write(traceback.format_exc())
        return 1  # error


#
sg.theme('DarkAmber')  # Add a touch of color
sys.excepthook = excepthook

def convert_multiple(files, converts_folder, dst_file_extension, inp_type, messege, title):
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


def main():
    file = on_open()
    #
    onlydir = Path.dirname(file)
    onlyname, file_extension = Path.splitext(file)
    # print("use name:", name)
    guess_type = convert.guess_type(file)
    #
    # All the stuff inside your window.
    title = lambda _s, c=None: sg.T(_s, font="Courier 40", text_color="#00cc00" if not c else c)
    # noinspection PyTypeChecker
    layout = [
        # ([sg.T(f"WARTING:{mess}", text_color="#ff0000")] if mess else []),
        [title("Info:", "#0099ff")],
        # [sg.Text('Use:', text_color="#0066ff"), sg.T(cls_vname, key="-use-", text_color="#0066ff")],
        [sg.Text('filename:', text_color="#0099ff"),
         sg.InputText(Path.basename(file), key="-file-", text_color="#0099ff")],
        [sg.Button('resave', key="-resave-", button_color=(None, "#0099ff"))],
        [sg.T()],
        [sg.B("info", key="-info-")],
        [title("Convert:")],
        [sg.T("Convert To:"), sg.InputText(Path.basename(onlyname), key="-convert-file-"), sg.T("with extension:"),
         sg.InputText("", size=(None, 40), key="-convert-file-extension-")],
        [sg.T("Convert as:"),
         sg.Combo(convert.inp_type_list, size=(None, 40), key='-inp-type-', default_value=guess_type,
                  enable_events=True)],
        [sg.B("Convert", button_color=(None, "#00cc00"), key="-convert-")],
        [sg.B(f"Convert all {file_extension} files in folder", button_color=(None, "#00cc00"), key="-convert-all-")],
    ]

    # Create the Window
    window = sg.Window('Convert Gui', layout).finalize()
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
                sg.popup_error("you need to type a filename for convert", title="need to type filename")
                continue
            #
            dst_file = None
            converts_folder = ""
            if dst_file_extension:
                if dst_file_extension[0] == ".":
                    dst_file_extension = dst_file_extension[1:]

            if event == "-convert-":
                dst_file = Path.join(onlydir, to_file) + "." + dst_file_extension if dst_file_extension else ''
                n = convert_safe(file, dst_file, inp_type)
                if n == 1:  # error
                    continue
                # convert_object = set_as_dst_file(convert_object, dst_file)
                # getattr(convert_object, convert_func.__name__)()

            elif event == "-convert-all-":
                converts_folder = Path.join(onlydir, "converts")
                if not Path.exists(converts_folder):
                    os.mkdir(converts_folder)
                glob_p = Path.join(onlydir, "*" + file_extension)
                print("glob search", glob_p)
                files_list = glob.glob(glob_p)
                if not files_list:
                    sg.popup("cant find files in this folder", f"(with pattern:\"{glob_p}\")")
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

        elif event == "-info-":
            filename = values["-file-"]
            folder = onlydir
            if not Path.isabs(folder):
                folder = Path.abspath(folder)
            folder = str(pathlib.WindowsPath(folder))
            window.hide()
            # try:
            mt_d = info.info(Path.join(folder, filename))
            info.gui(mt_d)
            # except AttributeError:
            #    import traceback

            #    traceback.print_exc()
            window.un_hide()

        # ic(event, values)

    window.close()


def multiple(files: list):
    try:
        guess_type = convert.guess_type(files[0])
    except Exception:
        guess_type = None
    #
    onlydir = os.path.dirname(files[0])
    #
    layout = [
        [sg.T("Convert All selected files To:"), sg.InputText("", size=(None, 40), key="-convert-file-extension-")],
        [sg.T("Convert All as:"),
         sg.Combo(convert.inp_type_list, size=(None, 40), key='-inp-type-', default_value=guess_type, )],
        [sg.B("Convert All", button_color=(None, "#00cc00"), key="-convert-", bind_return_key=True)],
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
