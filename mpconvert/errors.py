from rich.traceback import Traceback
from rich.console import Console
import traceback
import sys
import PySimpleGUI as sg


def excepthook(t, v, tb):
    if t == KeyboardInterrupt:
        return
    try:
        tb_console = Console(file=sys.stderr, record=True)
        tb_console.print(Traceback.from_exception(t, v, tb, show_locals=True))
        full_tb = tb_console.export_text()
    except Exception:  # fallback
        print("FATAL (rich error):", traceback.format_exc())
        full_tb = traceback.format_exception(t, v, tb)
    ms = f"""an error has occurred {t}({v}) \n full traceback (including variables) is in error.txt"""

    with open("error.txt", "w") as err_io:
        err_io.write(f"{ms}:\ntraceback:\n\n{full_tb}")

    try:
        sg.popup_error(ms, title="an error has occurred")
    except Exception as s:
        print("FATAL (pysimplegui error):" + str(s))

    print("done write and closed")
