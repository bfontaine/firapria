# -*- coding: UTF-8 -*-

from mock import patch, MagicMock
import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

from firapria import pollution
from firapria.pollution import PollutionFetcher


_urlopen = pollution.urlopen


class FakePage():
    def __init__(self, content=""):
        self.content = content

    def read(self):
        return self.content


class TestPollution(unittest.TestCase):

    def setUp(self):
        mock = MagicMock()
        mock.return_value = FakePage()
        pollution.urlopen = mock
        self.page_mock = mock

    def tearDown(self):
        pollution.urlopen = _urlopen

    # __init__

    def test_should_not_fetch_anything_on_creation(self):
        p = PollutionFetcher()
        self.assertEqual(self.page_mock.call_count, 0)

    # indices

    def test_should_return_none_if_cant_parse_page(self):
        res = PollutionFetcher().indices()
        self.assertTrue(self.page_mock.called)
        self.assertIs(res, None)
