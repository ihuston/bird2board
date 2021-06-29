import logging
import pathlib

import requests

from bird2board import Pinboard, Twitter


class Bird2Board:

    def __init__(self, pinboard_token, replace=False, shared=False, toread=False):
        self.pinboard = Pinboard(auth_token=pinboard_token, replace=replace, shared=shared, toread=toread)
        self.twitter = Twitter()

    def convert_single_file(self, file_path: pathlib.Path):
        try:
            json_text = file_path.read_text()
        except IOError:
            logging.error(f"Error reading file {file_path}")
            raise
        else:
            logging.info(f"Loaded JSON from file {file_path}.")

        try:
            tweets = self.twitter.parse_json(json_text)
        except Exception:
            logging.exception(f"Error parsing bookmark data from file {file_path}.")
            raise
        else:
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
        logging.info(f"Converted tweets from {file_path}.")
        return

    def convert_directory(self, tweet_directory: pathlib.Path):
        if tweet_directory.is_file():
            self.convert_single_file(tweet_directory)
        else:
            files_with_errors = []
            dir_size = len(list(tweet_directory.iterdir()))
            logging.info(f"Converting directory with {dir_size} possible files.")
            for i, p in enumerate(tweet_directory.iterdir()):
                if p.suffix == ".json":
                    try:
                        self.convert_single_file(p)
                    except (ValueError, KeyError, IOError, requests.exceptions.HTTPError):
                        logging.info(f"Error with file {p}, moving to next file.")
                        files_with_errors.append(p)
                    logging.info(f"Converted file {i+1} of {dir_size}.")
                else:
                    logging.info(f"Skipped file {p}.")
                logging.debug(f"Files with errors so far: {files_with_errors}")
            if len(files_with_errors) > 0:
                logging.info(f"Files with errors during processing: {files_with_errors}")
