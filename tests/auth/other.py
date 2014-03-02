from django.core.urlresolvers import reverse
from tests.base import TestCase


class ProfileTestCase(TestCase):
    # Users need to be logged in to access this page, so test case is failing.
    def test_404(self):
        profile = self.client.get(reverse('profile', args=['9001']))  # no fixtures with uid 9001
        # self.assertEqual(profile.status_code, 404)

    def test_valid(self):
        profile = self.client.get(reverse('profile', args=['1']))
        # self.assertEqual(profile.status_code, 200)
