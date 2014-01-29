from django import forms
from auth.models import Users
from common.forms import ModelForm


class RegisterForm(ModelForm):
    name = 'Sign Up'
    urlname = 'register'

    pwd = forms.CharField(label='password')
    confpwd = forms.CharField(label='confirm password')
    placeholders = {'confpwd': 'Confirm your password'}

    class Meta:
        model = Users
        fields = ('email', 'pwd', 'confpwd', 'fname', 'lname')

    def clean(self):
        print(self.fields['email'].required)
        print(self.cleaned_data)
