from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
import time
from auth.models import User
from common.forms import ModelForm


class LoginForm(ModelForm):
    name = 'Login'
    urlname = 'login'
    valid_users = (0,)
    success_url = 'index'

    pwd = forms.CharField(label='Password', widget=PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'pwd')

    def clean(self) -> dict:
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user is None and email is not None:
            raise ValidationError('The email does not exist in our database')
        if email is not None and not check_password(self.cleaned_data['pwd'], user.pwd):
            raise ValidationError('The password is incorrect')
        return self.cleaned_data

    def _post_clean(self):
        pass  # ensure we don't clean the email to make sure it is unique

    def save(self):
        sessionID = User.get(self.cleaned_data['email']).login()
        self.view.cookies['session'] = sessionID
