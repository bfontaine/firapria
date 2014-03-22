# -*- coding: UTF-8 -*-

from os.path import dirname
from mock import patch, MagicMock
import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

from firapria import pollution
from firapria.pollution import PollutionFetcher


_urlopen = pollution.urlopen

SAMPLE = open(dirname(__file__)+'/sample1.html').read()

class FakePage():
    def __init__(self, content=""):
        self.content = content

    def read(self):
        return self.content


class TestPollution(unittest.TestCase):

    def setReturnHTML(self, content):
        mock = MagicMock()
        mock.return_value = FakePage(content)
        pollution.urlopen = mock
        self.page_mock = mock

    def setUp(self):
        self.sample = SAMPLE
        self.setReturnHTML("")

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

    def test_should_fetch_indices_only_once(self):
        p = PollutionFetcher()
        p.indices()
        p.indices()
        self.assertEqual(self.page_mock.call_count, 1)

    def test_should_parse_eu_indices(self):
        self.setReturnHTML(self.sample)
        p = PollutionFetcher()
        res = p.indices(_type=PollutionFetcher.EU)
        self.assertEqual(self.page_mock.call_count, 1)
        self.assertSequenceEqual(res, [42, 40, 40])

    def test_should_parse_fr_indices(self):
        self.setReturnHTML(self.sample)
        p = PollutionFetcher()
        res = p.indices(_type=PollutionFetcher.FR)
        self.assertEqual(self.page_mock.call_count, 1)
        self.assertSequenceEqual(res, [4, 4, 3])
