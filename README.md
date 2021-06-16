# mpconvert
mpconvert is a python program to convert convert media (music,movies and images).

It can also download a file from url or from youtube.

mpconvert runs only in windows.

## Installing
for the installation you need python and pip. see [this guide](https://phoenixnap.com/kb/how-to-install-python-3-windows) if you dont have them.

To install with pip
type in terminal:
```
(sudo) pip install "https://github.com/matan-h/mpconvert/archive/main.zip"
```
this will create two commandline scripts:`mpconvert` and `info`
## Usage
### Command line
You can use mpconvert from the commandline using the `mpconvert` command
with `mpconvert [src-file] [dst-file] -t [music|movie|image|archive]`. without the -t it will automatically infer the file type.

For example - `mpconvert Mozart.mp3 Mozart.wav` will convert the audio "Mozart" from format mp3 to wav format. If you dont trust the automatic infer you can tell `mpconvert` that the src-file is music by add `-t music` to the command.

You can also use mpconvert command to open the `mpconvert-gui`
with `mpconvert [src-file]`. Without the src-file it open a file Browser dialog.

### GUI
after you open the gui you will see:
![screenshot](https://github.com/matan-h/mpconvert/raw/main/images/img.png)

explanation:

![explanation](https://github.com/matan-h/mpconvert/raw/main/images/expl.png)
## Right click "Send to..." option
In order to add mpconvert in the "Send to..." right click menu just do:
`python -m mpconvert.win_sendto`  

## Built With
* [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) - for create the gui
* [click](https://palletsprojects.com/p/click/) - for create the cli
* [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) - for movie convert
* [Pillow](https://python-pillow.org) - for image converter
* [pydub](http://pydub.com) - for audio converter
* [filetype](https://github.com/h2non/filetype.py) - Infer the file type
* [pywin32](https://github.com/mhammond/pywin32) - finding metadata of file
* [youtube_dl](https://github.com/ytdl-org/youtube-dl) - download videos from youtube

## Author
matan h

## License
This project is licensed under the MIT License.
