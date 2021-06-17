#!/usr/bin/env python
import click

import pathlib
import logging

from bird2board.bird2board import Bird2Board


@click.command()
@click.option('--debug', is_flag=True, default=False, help='enable debug logging')
@click.option('--toread/--not-toread', default=False, help='set Pinboard bookmarks as "to read"')
@click.option('--shared/--not-shared', default=False, help='set Pinboard bookmarks as shared')
@click.option('--replace/--no-replace', default=False, help='replace existing Pinboard bookmark for an URL')
@click.option('-p', '--pinboard-token', required=True, help='user token for Pinboard API',
              envvar="BIRD2BOARD_PINBOARD_TOKEN")
@click.argument('path', type=click.Path(exists=True, path_type=pathlib.Path, dir_okay=True, file_okay=True))
def convert(path, pinboard_token, replace, shared, toread, debug):
    """Save Twitter Bookmark .json file(s) at PATH (file or directory) to account using PINBOARD TOKEN."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    b2b = Bird2Board(pinboard_token=pinboard_token, replace=replace, shared=shared, toread=toread)
    try:
        b2b.convert_directory(path)
    except Exception:
        logging.exception("Failed to complete conversion.")
        raise click.Abort()
    return 0


if __name__ == "__main__":
    convert(auto_envvar_prefix='BIRD2BOARD')
