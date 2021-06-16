from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mpconvert',
    version='0.0.0',
    license='MIT',
    description='# TODO description',
    author='matan h',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='matan.honig2@gmail.com',
    url='https://github.com/matan-h/mpconvert',
    packages=['mpconvert'],
    entry_points={
        "console_scripts": [
            "mpconvert = mpconvert.convert:main",
            # "info = mpconvert.info:cli",
        ]
    },
    install_requires=['ffmpeg-python','click', 'pywin32', 'youtube_dl', 'PySimpleGUI', 'filetype',
                      'Pillow', 'pydub'],

    # python_requires = '', # todo

)
