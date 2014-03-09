from codejail.jail_code import jail_code, configure
from django.conf import settings
from tasks.modeldir.programming import check_output
from tests.base import TestCase


class CodeJailTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        configure('python3', settings.PYTHON_SANDBOX_PATH)

    def test_installed(self):
        self.assertEqual(
            jail_code('python3', 'print("Hello,", input())', stdin=b'Matt\n').stdout,
            b'Hello, Matt\n'
        )

    def test_check_err(self):
        self.assertEqual(check_output(b'', '', -9), 5)
        self.assertEqual(check_output(b'', '', 1), 6)
        self.assertEqual(check_output(b'', '', 8), 7)

    def test_check_correct(self):
        self.assertEqual(check_output(b'J. Smith', 'J. Smith', 0), 0)

    def test_check_whitespace(self):
        self.assertEqual(check_output(b'J. Smith', 'J.Smith', 0), 1)
        self.assertEqual(check_output(b'J.Smith', 'J. Smith', 0), 1)

    def test_check_punctuation(self):
        self.assertEqual(check_output(b'J Smith', 'J. Smith', 0), 2)
        self.assertEqual(check_output(b'J. Smith', 'J? Smith', 0), 2)

    def test_check_case(self):
        self.assertEqual(check_output(b'J. Smith', 'J. smith', 0), 3)
        self.assertEqual(check_output(b'j. smith', 'J. Smith', 0), 3)

    def test_wrong(self):
        self.assertEqual(check_output(b'Bobby Tables', 'J. Smith', 0), 4)
        self.assertEqual(check_output(b'J. Smith', 'Tables Bobby', 0), 4)
