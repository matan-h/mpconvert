# mpconvert
mpconvert is a python program to convert convert media (music,movies and images).

mpconvert not support macos.

## Installing
for the installation you need python and pip. see [this guide](https://phoenixnap.com/kb/how-to-install-python-3-windows) if you dont have them.

To install with pip
type in terminal:
```
(sudo) pip install "https://github.com/matan-h/mpconvert/archive/main.zip"
```
this will create the commandline scripts:`mpconvert`
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

<!-- explanation: -->

<!-- ![explanation](https://github.com/matan-h/mpconvert/raw/main/images/expl.png) -->
## Right click "Send to..." option
In order to add mpconvert in the "Send to..." right click menu run `pip install pywin32` and then `win_sendto.py`

## Built With
* [click](https://palletsprojects.com/p/click/) - for create the cli
* [filetype](https://github.com/h2non/filetype.py) - Infer the file type
* [moviepy](https://zulko.github.io/moviepy) - for movie convert
* [Pillow](https://python-pillow.org) - for image converter
* [pydub](http://pydub.com) - for audio converter
* [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) - for create the gui
* [rich](https://github.com/PySimpleGUI/PySimpleGUI) - debug (traceback)
* [screeninfo](https://github.com/rr-/screeninfo) - detect window location

## Author
matan h

## License
This project is licensed under the MIT License.
