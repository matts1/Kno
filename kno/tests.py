import os
from unittest import defaultTestLoader, makeSuite, TestSuite
from django.test import TestCase
from django.test.runner import DiscoverRunner, reorder_suite
from django.utils.importlib import import_module
from kno import settings


# https://gist.github.com/carljm/1450104
class DiscoveryRunner(DiscoverRunner):
    """A test suite runner that uses unittest2 test discovery."""
    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        tests = []
        discovery_root = settings.TEST_DISCOVERY_ROOT
        if not test_labels:
            test_labels = [x[0][6:] for x in os.walk(discovery_root) if x[0].count('/') == 1]
            if '__pycache__' in test_labels:
                test_labels.remove('__pycache__')

        test_labels = ['tests.' + label for label in test_labels]

        for label in test_labels:
            test_root = import_module(label).__path__[0]

            tests.extend(defaultTestLoader.discover(
                test_root,
                top_level_dir=settings.BASE_PATH,
                pattern='*.py'
            )._tests)

        suite = TestSuite(tests)

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)

        return reorder_suite(suite, (TestCase,))
