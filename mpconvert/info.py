import os
import random
from os import path

import click

from . import metadata
import PySimpleGUI as sg


def info(file):
    if not path.isabs(file):
        file = path.abspath(file)
    md_dict = metadata.metadata(file)
    mtl = metadata.metadata_list
    if "xa" in mtl:
        mtl.remove("xa")
    cmp = dict(zip(mtl, mtl))
    if md_dict == {} or md_dict == cmp:
        print("cant find meta data,close metadata")
        return {}
    if os.access(file, os.R_OK) and not path.isdir(file):
        full_dict = metadata.info_by_contact(file)
    else:
        sg.popup("cant guess file because cant open it or its folder", title="warting", text_color="orange")
        full_dict = {}
    # ic(md_info,md_dict)
    full_dict.update(md_dict)
    return full_dict
    # print(f"metadata on file:\"{file}\"")
    # for k, v in full_dict.items():
    #    print(f"{k}:{v}")


def gui(d):
    if not d:
        print("close metadata gui")
        return
    sg.theme("DarkAmber")
    # random_theme = lambda: random.choice(sg.list_of_look_and_feel_values())
    # r = random_theme()
    # print("use theme:", r)
    # sg.theme(r)
    f = 100
    n = 255
    random_color = lambda: sg.RGB(random.randint(f, n), random.randint(f, n), random.randint(f, n))
    clayout = []
    for k, v in d.items():
        color = random_color()
        clayout.append([sg.T(k, text_color=color), sg.T(":" * 10, text_color="#0099ff"), sg.T(v, text_color=color)])
    layout = [
        [sg.T("Convert metadata viewer", font="Courier 40")],
        [sg.Column(clayout, scrollable=True, vertical_scroll_only=True, size=(500,None), key="-col-")],
        [sg.Button("Close", key="-close-")]
    ]

    window = sg.Window('Convert metadata viewer', layout).finalize()
    window["-col-"].expand(True, True, True)
    while True:
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED or event == "-close-":  # if user closes window or click close
            break
    window.close()


@click.command(context_settings={"help_option_names": ['-h', '--help']}, no_args_is_help=True)
@click.argument("file", type=click.Path(exists=True, resolve_path=True))
def cli(file):
    """
    info on file
    """
    from pprint import pprint
    pprint(info(file))


if __name__ == '__main__':
    cli()
    # click
    # info("run.cmd")
