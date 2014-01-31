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

    # def clean_email(self, email):
    #     if Users.objects.filter(email=email):
    #         raise ValidationError('That email address is taken')

    def clean(self):
        if self.cleaned_data['pwd'] != self.cleaned_data['confpwd']:
            raise ValidationError('The passwords were different')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(False)  # don't commit because we're about to commit
        user.set_password(self.cleaned_data['pwd'])
        user.save()
        return user
