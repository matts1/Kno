import os
from unittest import defaultTestLoader, makeSuite, TestSuite
from django.test import TestCase
from django.test.runner import DiscoverRunner, reorder_suite
from django.utils.importlib import import_module
import re
from kno import settings

def make_test_case(suite):
    tests = []
    for test in suite._tests:
        if isinstance(test, TestSuite):
            tests.extend(make_test_case(test))
        else:
            tests.append(test)
    return tests


class DiscoveryRunner(DiscoverRunner):
    """A test suite runner that uses unittest2 test discovery."""
    def build_suite(self, options, extra_tests=None, **kwargs):
        tests = []
        discovery_root = settings.TEST_DISCOVERY_ROOT
        test_labels = [x[0][6:] for x in os.walk(discovery_root) if x[0].count('/') == 1]
        if '__pycache__' in test_labels:
            test_labels.remove('__pycache__')

        test_labels = ['tests.' + label for label in test_labels]

        for label in test_labels:
            test_root = import_module(label).__path__[0]

            tests.extend(make_test_case(defaultTestLoader.discover(
                test_root,
                top_level_dir=settings.BASE_PATH,
                pattern='*.py'
            )))

        include = [re.compile(x, re.I) for x in options if not x.startswith('no')]
        exclude = [re.compile(x[2:], re.I) for x in options if x.startswith('no')]

        tests = [(str(type(test))[14:-2], test) for test in tests]

        if include:
            tests = [t for t in tests if any([p.search(t[0]) for p in include])]
        for pattern in exclude:
            tests = [t for t in tests if not pattern.search(t[0])]

        suite = TestSuite([x[1] for x in tests])

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)

        return reorder_suite(suite, (TestCase,))
