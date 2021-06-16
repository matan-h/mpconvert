import os
import sys
import tarfile
import zipfile
from os import path
from os.path import splitext

#
from typing import Optional

import click
import filetype
#
import ffmpeg
from PIL import Image
from pydub import AudioSegment
from . import handler

##
default_p = print


def default(src: str, dst: str, t: str):
    """
    default error handling
    """
    p = default_p
    if not t:
        p('you forget to enter the type in \"convert as\" box.')
        return

    elif dst.strip()=='':
        p('you forget to enter the file extension ')
        return

    p(f"convert format '{t}' with file '{src}' not not support by Mpconvert now.")


def convert(src, dst, inp_type)->int:
    """
    convert src to dst with convert type

    Args:
        src: src file
        dst: dst file
        inp_type: convert type

    Returns: 1 if error

    """
    try:
        if path.exists(dst):
            os.remove(dst)
        ###
        src_format = splitext(src)[1][1:].lower()
        dst_format = splitext(dst)[1][1:].lower()
        ##########
        if inp_type == "music":
            AudioSegment.from_file(src, format=src_format).export(dst, format=dst_format)

        elif inp_type == "movie":
            (
                ffmpeg
                    .input(src)
                    .output(dst)
                    .run(capture_stderr=True)

            )
        elif inp_type == "archive":
            if zipfile.is_zipfile(src):
                with zipfile.ZipFile(src, "r") as zip_ref:
                    zip_ref.extractall(src)
            #

            elif tarfile.is_tarfile(src):
                with tarfile.open(src) as tar:
                    tar.extractall(dst)
            else:
                default(src, dst, inp_type)
                return 1

        elif inp_type == "image":
            if not ('.' + dst_format in Image.registered_extensions()):
                default_p(f'unknown image extension: \"{dst_format}\"')
                return 1
            try:
                Image.open(src).save(dst)
            except OSError:
                Image.open(src).convert('RGB').save(dst)

        else:
            default(src, dst, inp_type)
            return 1  # default
    except Exception as e:
        handler.handler(e)
        return 1


inp_type_list = ["music", "movie", "image", "archive"]


def guess_type(full_file)->Optional[str]:
    """
    guess type of file

    Args:
        full_file: file path

    Returns:the guesses type, if can`t - return None

    """
    mime: str = filetype.guess_mime(full_file)
    if not mime:
        return
        #
    mime: list = mime.split("/")
    d = {
        mime[0] == "audio": "music",
        mime[0] == "video": "movie",
        mime[0] == "image": "image",
        mime[0] == "application" and mime[1] in ["zip", "x-tar", "x-bzip2", "gzip", "x-xz"]: "archive",
    }
    if any(list(d.keys())):
        for k in d:
            if k:
                return d[k]
    else:
        return


@click.command(context_settings={"help_option_names": ['-h', '--help']}, )
@click.argument("file", type=click.Path(), required=False)
@click.argument("dst-file", type=click.Path(), required=False)
@click.option("--convert-type", "--inp-type", "--type", "-t", type=click.Choice(inp_type_list, case_sensitive=False))
def cli(file, dst_file, convert_type=None):
    """
    mpconvert - python media converter
    """
    if (file is None) or (dst_file is None):
        from . import maingui
        maingui.main()
        return

    if not convert_type:
        convert_type = guess_type(file)

    handler.p = default_p

    convert(file, dst_file, convert_type)


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("files", nargs=-1)
def sendto(files):
    """
    sendto cli.
    """
    from . import maingui
    if len(files) <= 1:  # not multiple
        maingui.main()
    else:
        maingui.multiple(files)


def main():
    """
    main program for mpconvert
    """
    if sys.argv[1:]:
        if sys.argv[1].upper() == '/$MULTIPLE':
            sys.argv.pop(0)
            sendto()
            quit()
    cli()


if __name__ == '__main__':
    main()
