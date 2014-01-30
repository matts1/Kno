from django import forms
from django.forms import PasswordInput
from auth.models import Users
from common.forms import ModelForm


class RegisterForm(ModelForm):
    name = 'Sign Up'
    urlname = 'register'
    valid_users = (0,)

    pwd = forms.CharField(label='password', widget=PasswordInput())
    confpwd = forms.CharField(label='confirm password', widget=PasswordInput())
    placeholders = {'confpwd': 'Confirm your password'}

    class Meta:
        model = Users
        fields = ('email', 'pwd', 'confpwd', 'fname', 'lname')

    def clean(self):
        print(self.fields['email'].required)
        print(self.cleaned_data)
