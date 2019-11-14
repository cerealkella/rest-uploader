# -*- coding: utf-8 -*-

"""Console script for rest_uploader."""
import sys
import click
from .rest_uploader import watcher
from .img_process import set_language
from . import __version__


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
@click.version_option(version=__version__)
def main(path=None, language="eng"):
    """ Console script for rest_uploader.
        Define file path to monitor, e.g.
        rest_uploader /home/user/Docouments/scans    
    """
    click.echo("Launching Application " "rest_uploader.cli.main")
    set_language(language)
    click.echo("Language: " + language)
    watcher(path=path)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
