from django.contrib.auth.models import AbstractBaseUser
from django.db import models

# if this is User instead of Users, everything fails
class Users(AbstractBaseUser):
    email = models.EmailField(max_length=100, primary_key=True, unique=True)
    fname = models.CharField('First Name', max_length=50)
    lname = models.CharField('Last Name', max_length=50)
    teacher = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    def get_full_name(self) -> str:
        return '{} {}'.format(self.fname, self.lname)

    def get_short_name(self) -> str:
        return self.fname
