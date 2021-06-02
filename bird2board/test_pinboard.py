import os
import unittest
from unittest import TestCase

from . import bird2board


class TestPinboard(TestCase):

    @unittest.skipIf("PINBOARD_TOKEN" not in os.environ,
                     "requires a real user API token for connection")
    def test_pinboard_connection(self):
        token = os.getenv("PINBOARD_TOKEN", "mytoken")
        pinboard = bird2board.Pinboard(token)
        assert pinboard.check_connection()

    def test_prepare_url(self):
        pinboard = bird2board.Pinboard("mytoken")
        url = pinboard.prepare_url(action="update")
        assert url == pinboard.api_url + "update?auth_token=mytoken&format=json"

