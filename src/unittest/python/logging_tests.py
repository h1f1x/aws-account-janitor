from io import StringIO
import unittest
from unittest.mock import patch

from aws_account_janitor.logging import log


class LoggingTests(unittest.TestCase):

    def test_log(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            log('foo')
            self.assertEqual('foo\n', fake_out.getvalue())
