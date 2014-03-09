from django.core.urlresolvers import reverse, resolve
from django.test import RequestFactory
from auth.models import User
from tests.base import TestCase


class RequestTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = RequestFactory()

    def fetch(self, name, *args, data={}, post=False, **kwargs):
        url = reverse(name, args=args, kwargs=kwargs)
        view = resolve(url).func
        request = self.f.post(url, data) if post else self.f.get(url, data)
        self.user = User.objects.get(email='student@gmail.com') if not hasattr(self, 'user') else \
            self.user
        request.user = self.user
        return view(request, *args, **kwargs)
