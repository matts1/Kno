from django import forms
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
from auth.models import Users
from common.forms import ModelForm


class RegisterForm(ModelForm):
    name = 'Sign Up'
    urlname = 'register'
    valid_users = (0,)
    success_msg = 'You have registered'

    pwd = forms.CharField(label='password', widget=PasswordInput())
    confpwd = forms.CharField(label='confirm password', widget=PasswordInput())
    placeholders = {'confpwd': 'Confirm your password'}

    class Meta:
        model = Users
        fields = ('email', 'pwd', 'confpwd', 'fname', 'lname')

    def clean(self):
        print('general clean')
        return self.cleaned_data

    def clean_email(self):
        print('cleaning email')

    def clean_pwd(self):
        print('cleaning pwd')
        raise ValidationError([ValidationError('blah'), ValidationError('b2')])
