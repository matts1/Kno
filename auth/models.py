from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class User(AbstractBaseUser):
    email = models.CharField(max_length=100, primary_key=True)
    fname = models.CharField(max_length=50, blank=False)
    lname = models.CharField(max_length=50, blank=False)
    teacher = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def get_full_name(self):
        return '{} {}'.format(self.fname, self.lname)

    def get_short_name(self):
        return self.lname
