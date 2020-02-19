# -*- coding: utf-8 -*-

"""Console script for rest_uploader."""
import sys
import click
from .rest_uploader import watcher, set_autotag
from .img_process import set_language
from . import __version__


"""Helper function for wild arguments"""
def parse_argument(arg):
    if arg in ["No", "N", "NO", "OFF", "off", "n", "no"]:
        arg = "no"
    else:
        arg = "yes"
    return arg


@click.command()
@click.argument(
    "path",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
)
@click.option(
    "-l",
    "--language",
    "language",
    default="eng",
    help="""Specify OCR Language. 
            Refer to Tesseract's documentation found here:
            https://github.com/tesseract-ocr/tesseract/wiki""",
)
@click.option(
    "-t",
    "--autotag",
    "autotag",
    default="yes",
    help="""Specify whether or not to automatically tag notes
            based on OCR'd text. Default = 'yes', specify 'no' 
            if this behavior is not desired""",
)
@click.version_option(version=__version__)
def main(path=None, language="eng", autotag="yes"):
    """ Console script for rest_uploader.
        Define file path to monitor, e.g.
        rest_uploader /home/user/Docouments/scans    
    """
    click.echo("Launching Application " "rest_uploader.cli.main")
    set_language(language)
    autotag = parse_argument(autotag)
    set_autotag(parse_argument(autotag))
    click.echo("Language: " + language)
    click.echo("Automatically Tag Notes? " + autotag)
    watcher(path=path)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
