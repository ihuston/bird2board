#!/usr/bin/env python
import click

from bird2board import Twitter
from bird2board import Pinboard

import pathlib
import logging


logging.basicConfig(level=logging.INFO)


class Bird2Board:

    def __init__(self, pinboard_token):
        self.pinboard = Pinboard(auth_token=pinboard_token)
        self.twitter = Twitter()

    def convert_single_file(self, file_path: pathlib.Path):
        try:
            json_text = file_path.read_text()
        except IOError:
            logging.error(f"Error reading file {file_path}")
            raise

        logging.info("Loaded JSON from file.")

        tweets = self.twitter.parse_json(json_text)
        logging.info(f"Parsed {len(tweets)} tweets from file.")

        for tweet in tweets:
            bookmark = self.pinboard.tweet_to_bookmark(tweet)
            try:
                self.pinboard.add_bookmark(bookmark)
            except Exception:
                logging.error(f"Error saving bookmark to Pinboard {bookmark['url']}")
                raise
            else:
                logging.info(f"Saved bookmark to Pinboard: {bookmark['url']}")
        return

    def convert_directory(self, tweet_directory: pathlib.Path):
        for p in tweet_directory.iterdir():
            if p.suffix == ".json":
                self.convert_single_file(p)


@click.command()
@click.option('-p', '--pinboard-token', required=True, help='user token for Pinboard API')
@click.argument('path', type=click.Path(exists=True, path_type=pathlib.Path, dir_okay=True, file_okay=True))
def convert(path, pinboard_token):
    """Save Twitter Bookmark .json file(s) at PATH (file or directory) to account using PINBOARD TOKEN."""
    b2b = Bird2Board(pinboard_token)
    try:
        b2b.convert_directory(path)
    except Exception:
        logging.error("Failed to complete conversion.")
        raise click.Abort()
    return 0


if __name__ == "__main__":
    convert(auto_envvar_prefix='BIRD2BOARD')
