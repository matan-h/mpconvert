from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mpconvert',
    version='0.0.0',
    license='MIT',
    description='simple media converter app',
    author='matan h',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='matan.honig2@gmail.com',
    url='https://github.com/matan-h/mpconvert',
    packages=['mpconvert'],
    entry_points={
        "console_scripts": [
            "mpconvert = mpconvert.__main__:converter",
            # "info = mpconvert.info:cli",
        ]
    },
    install_requires=['click', 'filetype', 'moviepy',
                      'Pillow', 'pydub', 'PySimpleGUI', 'rich', 'screeninfo'],

    # python_requires = '', # todo

)
