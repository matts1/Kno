from auth.forms import RegisterForm
from auth.models import User
from common.templatetags.form import func
from tests.base_request import RequestTestCase


class TemplateTagTestCase(RequestTestCase):
    user = None

    def test_func(self):
        self.assertEqual(func('list', 'abc'), ['a', 'b', 'c'])

    def test_as_modal(self):
        self.assertEqual(RegisterForm(
            user=User.objects.get(email='teacher@gmail.com')).as_modal(),
            ''
        )
        # ensure this doesn't chuck an error
        self.fetch('register')

    def test_as_form(self):
        self.assertEqual(RegisterForm(
            user=User.objects.get(email='teacher@gmail.com')).as_form(),
            ''
        )
