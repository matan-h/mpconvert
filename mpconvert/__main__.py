from . import convert

from .utils import guess_type
import click


@click.command(context_settings={"help_option_names": ['-h', '--help']}, )
@click.argument("file", type=click.Path(), required=False)
@click.argument("dst-file", type=click.Path(), required=False)
@click.option("--convert-type", "--inp-type", "--type", "-t", type=click.Choice(list(convert.convertmap.keys()), case_sensitive=False))
def converter(file, dst_file, convert_type=None):
    """
    mpconvert - simple media converter app
    """
    if (file is None) or (dst_file is None):
        from .main import main
        return main(file)
    if not convert_type:
        convert_type = guess_type(file)
    convert.convertmap[convert_type](file, dst_file)


if __name__ == "__main__":
    converter()
