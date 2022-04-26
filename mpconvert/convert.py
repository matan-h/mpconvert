import os
from PIL import Image
import PIL
from pydub import AudioSegment
import pydub.exceptions
import moviepy.editor as moviepy
from .utils import get_extension


def convert_music(src, dst):
    AudioSegment.from_file(src).export(dst, format=get_extension(dst))


def convert_video(src, dst):
    moviepy.VideoFileClip(src).write_videofile(dst)


def convert_image(src, dst):
    try:
        Image.open(src).save(dst)
    except OSError:
        Image.open(src).convert('RGB').save(dst)


convertmap = {
    "music": convert_music,
    "video": convert_video,
    "image": convert_image,
}
