# -*- coding: UTF-8 -*-

from os.path import dirname
import platform

if platform.python_version() < '3.3':
    from mock import MagicMock
else:
    from unittest.mock import MagicMock

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

from firapria import pollution
from firapria.pollution import get_indices


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

    def test_get_indices(self):
        res = get_indices()
        self.assertTrue(self.page_mock.called)
        self.assertIs(res, None)

    # indices

    def test_should_return_none_if_cant_parse_page(self):
        res = get_indices()
        self.assertTrue(self.page_mock.called)
        self.assertIs(res, None)

    def test_should_parse_eu_indices(self):
        self.setReturnHTML(self.sample)
        res = get_indices()
        self.assertEqual(self.page_mock.call_count, 1)
        self.assertSequenceEqual(list(res), [42, 40, 40])
