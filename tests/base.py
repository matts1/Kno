from django.test import TestCase
from auth.models import User


class TestCase(TestCase):
    fixtures = ['data']
    lazydata = {}

    def lazy(self, data, field='email', model=User):
        key = '{}_{}_{}'.format(model.__class__.__name__, field, data)
        if key not in self.lazydata:
            self.lazydata[key] = model.get(**{field: data})
        return self.lazydata[key]
