from auth.forms import RegisterForm
from common.views import FormView


class RegisterView(FormView):
    form_class = RegisterForm
