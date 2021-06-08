#!/usr/bin/env python
import click

import pathlib
import logging

from bird2board.bird2board import Bird2Board

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option('-p', '--pinboard-token', required=True, help='user token for Pinboard API')
@click.argument('path', type=click.Path(exists=True, path_type=pathlib.Path, dir_okay=True, file_okay=True))
def convert(path, pinboard_token):
    """Save Twitter Bookmark .json file(s) at PATH (file or directory) to account using PINBOARD TOKEN."""
    b2b = Bird2Board(pinboard_token)
    try:
        b2b.convert_directory(path)
    except Exception:
        logging.exception("Failed to complete conversion.")
        raise click.Abort()
    return 0


if __name__ == "__main__":
    convert(auto_envvar_prefix='BIRD2BOARD')
