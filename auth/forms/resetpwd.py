from django import forms
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
from auth.models import User
from common.forms import ModelForm


class ResetPwdForm(ModelForm):
    name = 'Sign Up'
    urlname = 'resetpwd'
    success_msg = 'Your password has been changed'

    oldpwd = forms.CharField(label='old password', widget=PasswordInput())
    newpwd = forms.CharField(label='new password', widget=PasswordInput())
    confpwd = forms.CharField(label='confirm password', widget=PasswordInput())
    placeholders = {'confpwd': 'Confirm Your New Password'}

    class Meta:
        model = User
        fields = ('oldpwd', 'newpwd', 'confpwd')

    def clean(self) -> dict:
        if not check_password(self.cleaned_data.get('oldpwd'), self.user.pwd):
            raise ValidationError('Incorrect Password')
        if not self.cleaned_data.get('newpwd'):
            raise ValidationError('New password cannot be empty')
        if self.cleaned_data.get('newpwd') != self.cleaned_data.get('confpwd'):
            raise ValidationError('The passwords were different')
        return self.cleaned_data

    def _clean_fields(self):  # don't try to validate the fields
        pass

    def save(self):
        self.user.pwd = make_password(self.cleaned_data['newpwd'])
        self.user.save()
