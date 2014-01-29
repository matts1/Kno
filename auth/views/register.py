from auth.forms import RegisterForm
from common.views import FormView


class RegisterView(FormView):
    template_name = 'test.html'
    form_class = RegisterForm
