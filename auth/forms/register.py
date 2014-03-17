from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
from auth.models import User
from common.forms import ModelForm
from common.validators import matches_regex
from misc.models import Search


class RegisterForm(ModelForm):
    name = 'Sign Up'
    urlname = 'register'
    valid_users = (0,)
    success_msg = 'You have been registered. You can {{ Login }}log in</a> now'

    pwd = forms.CharField(label='password', widget=PasswordInput())
    confpwd = forms.CharField(label='confirm password', widget=PasswordInput())
    placeholders = {'confpwd': 'Confirm your password'}

    class Meta:
        model = User
        fields = ('email', 'pwd', 'confpwd', 'fname', 'lname', 'school')

    def clean(self) -> dict:
        if self.cleaned_data.get('pwd') != self.cleaned_data.get('confpwd'):
            raise ValidationError('The passwords were different')
        return self.cleaned_data

    clean_fname = clean_lname =  matches_regex(
        r'[a-z]+',
        'Please enter only letters in your name',
        lambda x: x.strip().title()
    )

    def save(self):
        user = User(
            email = self.cleaned_data['email'],
            pwd = make_password(self.cleaned_data['pwd']),
            fname = self.cleaned_data['fname'],
            lname=self.cleaned_data['lname'],
            school=self.cleaned_data['school']
        )
        if hasattr(self.view, 'cookies') and 'session' in self.view.cookies:
            self.view.cookies['session'] = None
        user.save()
        Search.add_words(user.get_full_name(), user.id, User)
