# -*- coding: UTF-8 -*-

import sys
import platform
from mock import patch, MagicMock

from firapria import cli
from firapria import __version__

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

from StringIO import StringIO
from colorama import Fore
from firapria import cli, pollution

_sys_exit = sys.exit
_sys_stdout = sys.stdout
_sys_argv = sys.argv

_cli_print_pollution = cli.print_pollution
_pollution_fetcher = cli.PollutionFetcher

class TestCli(unittest.TestCase):

    def setFakeIndices(self, indices):
        class FakePollutionFetcher():
            def indices(self, *args):
                return indices
        cli.PollutionFetcher = FakePollutionFetcher

    def setUp(self):
        exitMock = MagicMock()
        exitMock.return_value = None
        sys.exit = exitMock
        self.exitMock = exitMock
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.exit = _sys_exit
        sys.stdout = _sys_stdout
        sys.argv = _sys_argv
        cli.print_pollution = _cli_print_pollution
        cli.PollutionFetcher = _pollution_fetcher

    # print_version_and_exit

    def test_print_version(self):
        cli.print_version_and_exit()
        self.assertTrue(self.exitMock.called)
        self.stdout.seek(0)
        self.assertEqual(self.stdout.read(), "firapria v%s\n" % __version__)

    # colorize_indice

    def test_colorize_0(self):
        n = 0
        res = cli.colorize_indice(n, 100)
        self.assertEqual(res, "%s%d%s" % (Fore.WHITE, n, Fore.RESET))

    def test_colorize_higher_than_max(self):
        n = 140
        res = cli.colorize_indice(n, 100)
        self.assertEqual(res, "%s%d%s" % (Fore.YELLOW, n, Fore.RESET))

    def test_colorize_max(self):
        n = 100
        res = cli.colorize_indice(n, 100)
        self.assertEqual(res, "%s%d%s" % (Fore.YELLOW, n, Fore.RESET))

    def test_colorize_30(self):
        n = 3
        res = cli.colorize_indice(n, 10)
        self.assertEqual(res, "%s%d%s" % (Fore.GREEN, n, Fore.RESET))

    def test_colorize_55(self):
        n = 11
        res = cli.colorize_indice(n, 20)
        self.assertEqual(res, "%s%d%s" % (Fore.MAGENTA, n, Fore.RESET))

    def test_colorize_80(self):
        n = 4
        res = cli.colorize_indice(n, 5)
        self.assertEqual(res, "%s%d%s" % (Fore.RED, n, Fore.RESET))

    # print_pollution

    def test_print_pollution(self):
        indices = [45, 37, 73]
        self.setFakeIndices(indices)
        cli.print_pollution()
        self.stdout.seek(0)
        self.assertEqual(self.stdout.read(), """Pollution:
\tYesterday: %s%d%s
\tToday: %s%d%s
\tTomorrow: %s%d%s
""" % (Fore.GREEN, indices[0], Fore.RESET, Fore.GREEN, indices[1], Fore.RESET,
    Fore.MAGENTA, indices[2], Fore.RESET))

    # main

    def test_version_flag(self):
        sys.argv = ['firapria', '--version']
        cli.main()
        self.assertTrue(self.exitMock.called)
        self.stdout.seek(0)
        self.assertEqual(self.stdout.read(), "firapria v%s\n" % __version__)

    def test_main_print_pollution(self):
        mock = MagicMock()
        mock.return_value = None
        cli.print_pollution = mock
        cli.main()
        self.assertTrue(mock.called)
