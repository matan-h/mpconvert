import os
import pathlib
import sys
import traceback
import PySimpleGUI as sg


def on_open():
    if sys.argv[1:]:
        argv = sys.argv
        file = " ".join(argv[1:])
    else:
        file = popup_get_file("please choose a file to convert", "Mpconvert")
    #
    if not os.path.exists(file):
        s = f'file not found:"{file}"'
        print(s)
        sg.popup(s)
        exit(1)

    return file


def popup_get_file(message, title=None):
    layout = [[sg.Text(message)],
              [sg.Input(key="-file-"), sg.FileBrowse()],
              [sg.OK(key="-ok-"), sg.Cancel(key="-cancel-"), ]]

    window = sg.Window(title, layout)
    event, values = window.read()
    window.close()
    if event == "-cancel-" or event == sg.WIN_CLOSED:
        print("exiting")
        exit(0)

    return values["-file-"]


def excepthook(cls, value, tb):
    ms = f"""an error has occurred {cls}({value}) \n all traceback will write to error.txt"""
    print(ms)
    try:
        sg.popup_error(ms, title="an error has occurred")
    except Exception as s:
        print("FATAL:" + str(s))
    with open("error.txt", "w") as err_io:
        n = ""
        err_io.write(f"{ms}:\ntraceback:\n{n.join(traceback.format_exception(cls, value, tb))}")
    traceback.print_exception(cls, value, tb)
    print("done write and closed")


def popup_open_folder(title, folder, file):
    folder = str(pathlib.WindowsPath(folder))
    if file:
        file = str(pathlib.WindowsPath(file))
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
            os.system(f'start explorer /select,\"{file}\"')
        else:
            print("open folder in explorer:", folder)
            os.system(f'start explorer \"{folder}\"')

    elif event == "open-file":
        if file:
            os.startfile(file)
    return


def progress_bar(key, iterable, *args, title='', **kwargs):
    sg.OneLineProgressMeter(title, 0, len(iterable), key, *args, **kwargs)
    for i, val in enumerate(iterable):
        yield val
        if not sg.OneLineProgressMeter(title, i + 1, len(iterable), key, *args, **kwargs):
            break
