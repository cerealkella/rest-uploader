# -*- coding: utf-8 -*-

"""Console script for rest_uploader."""
import sys
import click
from .rest_uploader import (
    watcher,
    set_autotag,
    set_notebook_id,
    set_working_directory,
    set_endpoint,
    set_token,
)
from .img_process import set_language, set_temp_path
from . import __version__


def parse_argument(arg):
    """Helper function for wild arguments"""
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
    "-s",
    "--server",
    "server",
    default="127.0.0.1",
    help="""Specify the server to which the application 
            should connect. Default = "127.0.0.1". """,
)
@click.option(
    "-p",
    "--port",
    "port",
    default="41184",
    help="""Specify the port to which the application 
            should connect. Default = "41184". """,
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
@click.option(
    "-d",
    "--destination",
    "destination",
    default="inbox",
    help="""Specify the notebook in which to place
            This notebook must exist or program will exit
            newly created notes. Default = "inbox". """,
)
@click.version_option(version=__version__)
def main(
    path=None,
    server="server",
    port="port",
    language="eng",
    autotag="yes",
    destination="inbox",
):
    """ Console script for rest_uploader.
        Define file path to monitor, e.g.
        rest_uploader /home/user/Docouments/scans    
    """
    click.echo("Launching Application " "rest_uploader.cli.main")
    set_working_directory()
    set_endpoint(server, port)
    set_token()
    set_temp_path()
    notebook_id = set_notebook_id(destination.strip())
    if notebook_id == -1:
        click.echo("Unable to run rest_uploader -- check to see if Joplin is running")
        return 0
    elif notebook_id == 0:
        click.echo(f"Invalid Notebook, check to see if {destination.strip()} exists.")
        return 0
    else:
        click.echo(f"Found Notebook ID: {notebook_id}")
    set_language(language)
    autotag = parse_argument(autotag)
    set_autotag(parse_argument(autotag))
    click.echo("Language: " + language)
    click.echo("Automatically Tag Notes? " + autotag)
    click.echo("Desitnation Notebook: " + destination)
    watcher(path=path)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
