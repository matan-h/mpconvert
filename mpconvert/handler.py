import pydub.exceptions
import ffmpeg
import PySimpleGUI as sg
import PIL.Image

p = lambda s: sg.popup_ok(s)


def ffmpeg_base(messege:str, text:str)->str:
    """
    handle basic ffmpeg errors

    Args:
        messege: the python wrapper first line
        text: the output from ffmpeg

    Returns:text to display in popup

    """
    sep = ':\n'
    #
    text = list(filter(None, text.split('\n')))
    text_m2 = ''
    if len(text) >= 2:
        if ']' in text[-2]:
            text_m2 = text[-2].split(']')[1] + '\n'

    text = text[0] + '\n' + (text[-1] + '\n' if not text[-1].lower().startswith('ffmpeg version') else '') + text_m2
    text = messege + sep + text
    return text


def pydub_handler(e: pydub.exceptions.PydubException)->str:
    """
    parse pydub error to the pattern of ffmpeg basic errors
    """
    text: str = e.args[0]
    messege = text.split('\n')[0]
    text = '\n'.join(text.split('\n')[1:])
    return ffmpeg_base(messege, text)


def python_ffmpeg_handler(e: ffmpeg.Error)->str:
    """
    parse python-ffmpeg error to the pattern of ffmpeg basic errors
    """
    messege = e.args[0].split('(')[0]
    return ffmpeg_base(messege, e.stderr.decode('utf8'))


def handler(e)->int:
    """
    main error handler.
    open popup with text

    Args:
        e: the exception
    Returns: 1



    """
    te = type(e)
    base = te.__base__
    # pydub
    if base == pydub.exceptions.PydubException:
        text = pydub_handler(e)

    # ffmpeg-python
    elif te == ffmpeg.Error:
        text = python_ffmpeg_handler(e)

    # PIL error
    elif te == PIL.UnidentifiedImageError:
        text = e.args[0]

    # file not found
    elif te == FileNotFoundError:
        text = f'the file "{e.filename}" not found '
    # ose error
    elif te == OSError or base == OSError:
        text = f"{e.strerror}: \"{e.filename}\""

    else:
        text = type(e).__qualname__ + ':' + str(e)
    #
    if text:
        p(text)
    return 1
