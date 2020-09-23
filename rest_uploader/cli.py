# -*- coding: utf-8 -*-

"""Console script for rest_uploader."""
import sys
import click
import tempfile
from .rest_uploader import (
    watcher,
    set_autotag,
    set_notebook_id,
    set_working_directory,
    set_endpoint,
    set_token,
    set_language,
    set_autorotation,
    set_moveto,
)
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
    help="""Specify the server to which the application"""
    """ should connect. Default = "127.0.0.1" """,
)
@click.option(
    "-p",
    "--port",
    "port",
    default="41184",
    help="""Specify the port to which the application should connect."""
    """ Default = 41184 """,
)
@click.option(
    "-l",
    "--language",
    "language",
    default="eng",
    help="""Specify OCR Language. Refer to Tesseract's documentation found here: 
    https://github.com/tesseract-ocr/tesseract/wiki""",
)
@click.option(
    "-t",
    "--autotag",
    "autotag",
    default="yes",
    help="""Specify whether or not to automatically tag notes based on"""
    """ OCR'd text. Default = 'yes', specify 'no' if this behavior is"""
    """ not desired""",
)
@click.option(
    "-d",
    "--destination",
    "destination",
    default="inbox",
    help="""Specify the notebook in which to place newly created notes."""
    """ Specified notebook must exist or program will exit."""
    """ Default = "inbox". """,
)
@click.option(
    "-r",
    "--autorotation",
    "autorotation",
    default="yes",
    help="""Specify whether to rotate images."""
    """ Default = yes (autorotation on, specify 'no' to disable). """,
)
@click.option(
    "-m",
    "--moveto",
    "moveto",
    default=tempfile.gettempdir(),
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=True,
    )
)
@click.version_option(version=__version__)
def main(
    path=None,
    server="server",
    port="port",
    language="eng",
    autotag="yes",
    destination="inbox",
    autorotation="yes",
    moveto="",
):
    """ Console script for rest_uploader.
        Define file path to monitor, e.g.
        rest_uploader /home/user/Docouments/scans    
    """
    click.echo("Launching Application " "rest_uploader.cli.main")
    set_working_directory()
    set_endpoint(server, port)
    set_token()
    # set_temp_path() # Do I need to do this here?
    notebook_id = set_notebook_id(destination.strip())
    if notebook_id == "err":
        click.echo("Joplin may not be running, please ensure it is open.")
        click.echo("     will check again when processing a file.")
    elif notebook_id == "":
        click.echo(f"Invalid Notebook, check to see if {destination.strip()} exists.")
        click.echo(f"Please specify a valid notebook. Quitting application.")
        return 0
    else:
        click.echo(f"Found Notebook ID: {notebook_id}")
    set_language(language)
    autotag = parse_argument(autotag)
    set_autotag(parse_argument(autotag))
    autorotation = parse_argument(autorotation)
    set_autorotation(autorotation)
    moveto = set_moveto(moveto)
    click.echo("Language: " + language)
    click.echo("Automatically Tag Notes? " + autotag)
    click.echo("Destination Notebook: " + destination)
    click.echo("Autorotation: " + autorotation)
    if moveto == "":
        click.echo("Files will remain in the monitoring directory")
    else:
        click.echo("File move to location: " + moveto)
    watcher(path=path)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
