#!/usr/bin/env python
import os

import requests


class Pinboard:
    format = "json"
    api_url = "https://api.pinboard.in/v1/posts/"

    def __init__(self, auth_token=None):
        if auth_token is None:
            self.auth_token = os.getenv("PINBOARD_TOKEN")
        else:
            self.auth_token = auth_token

    def check_connection(self):
        req = requests.request("GET", self.prepare_url("update"))
        return req.ok

    def prepare_url(self, action):
        return f"{self.api_url}{action}?auth_token={self.auth_token}&format={self.format}"


def main():
    pass


if __name__ == "__main__":
    main()


