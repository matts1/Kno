from django import forms
from django.contrib.auth.hashers import make_password
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
        fields = ('pwd', 'confpwd', 'reset_code')

    def clean(self):
        if self.cleaned_data.get('pwd') != self.cleaned_data.get('confpwd'):
            raise ValidationError('Passwords were different')
        return self.cleaned_data

    def clean_reset_code(self, value):
        if value is None:
            raise ValidationError('Need to provide a reset code')
        if not User.objects.filter(reset_code=value):
            raise ValidationError(
                'Reset code is invalid. You may not have copied the whole url, or there may have '
                'been another reset code sent since'
            )

    def save(self):
        user = User.objects.get(reset_code=self.cleaned_data['reset_code'])
        user.pwd = make_password(self.cleaned_data['pwd'])
        user.reset_code = None
        user.save()
