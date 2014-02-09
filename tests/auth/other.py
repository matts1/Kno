from django.core.urlresolvers import reverse
from tests.base import TestCase


class ProfileTestCase(TestCase):
    def test_404(self):
        profile = self.client.get(reverse('profile', args=['99']))  # no fixtures with uid 99
        self.assertEqual(profile.status_code, 404)

    def test_valid(self):
        profile = self.client.get(reverse('profile', args=['1']))
        self.assertEqual(profile.status_code, 200)
