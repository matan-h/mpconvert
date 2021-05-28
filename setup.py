from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='convert',
    version='0.0.0',
    license='MIT',
    description='# TODO description',
    author='matan h',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='matan.honig2@gmail.com',
    url='https://github.com/matan-h/convert',
    packages=['convert'],
    entry_points={
        "console_scripts": [
            "convert-file = convert.convert:main",
            "info = convert.info:cli",
        ]
    },
    install_requires=['ffmpeg-python','click', 'pywin32', 'youtube_dl', 'PySimpleGUI', 'filetype',
                      'Pillow', 'pydub'],

    # python_requires = '', # todo

)
