from django import forms
from django.core.exceptions import ValidationError
from auth.models import User
from common.forms import ModelForm


class ForgotPwdForm(ModelForm):
    name = 'Reset Password'
    button = 'Send Reset Code'
    urlname = 'forgotpwd'
    valid_users = (0,)
    success_msg = 'An email has been sent with a password reset link'
    update = True

    class Meta:
        model = User
        fields = ('email',)

    def clean(self):
        if 'email' in self.cleaned_data and not User.get(self.cleaned_data['email']):
            raise ValidationError('The email address does not exist in our database')
        return self.cleaned_data

    def save(self):
        User.get(self.cleaned_data['email']).forgotpwd()


class DoResetPwdForm(ModelForm):
    name = 'Reset Password'
    urlname = 'doresetpwd'
    valid_users = (0, 1, 2)
    success_msg = 'Your password has been reset'
    update = True

    pwd = forms.CharField(label='password', widget=forms.PasswordInput())
    confpwd = forms.CharField(label='confirm password', widget=forms.PasswordInput())
    placeholders = {'confpwd': 'Confirm your password'}

    class Meta:
        model = User
        fields = ('pwd', 'confpwd')
