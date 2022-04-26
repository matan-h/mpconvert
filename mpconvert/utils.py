import os
from typing import Optional
import screeninfo
import filetype
location = None
try:
    for m in screeninfo.get_monitors():
        # print(m)
        if m.is_primary:
            location = (m.width / 2, m.height / 2)
except screeninfo.ScreenInfoError:
    pass


def guess_type(full_file) -> Optional[str]:
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
        mime[0] == "video": "video",
        mime[0] == "image": "image",
    }
    if any(list(d.keys())):
        for k in d:
            if k:
                return d[k]
    else:
        return


def get_extension(f):
    return os.path.splitext(f)[1][1:].lower()


if __name__ == "__main__":
    import sys
    # print(guess_type(' '.join(sys.argv[1:])))
    # print(get_location())
