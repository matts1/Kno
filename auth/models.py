import os
import binascii
from common import models
from django.utils import timezone
from datetime import timedelta

class User(models.Model):
    email = models.EmailField(max_length=100, primary_key=True, unique=True,
                              error_messages={'unique': 'The email address is already taken'})
    pwd = models.CharField('Password', max_length=128)
    fname = models.CharField('First Name', max_length=50)
    lname = models.CharField('Last Name', max_length=50)

    teacher = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('fname', 'lname', 'pwd')

    def get_full_name(self) -> str:
        return '{} {}'.format(self.fname, self.lname)

    def get_short_name(self) -> str:
        return self.fname

    def login(self):
        return Session.create(self)

class Session(models.Model):
    sessionID = models.CharField(max_length=100, primary_key=True, unique=True)
    user = models.ForeignKey(User)
    expiry = models.DateTimeField()

    @classmethod
    def create(cls, user):
        sessionID = None
        while sessionID is None or cls.objects.filter(sessionID=sessionID):
            sessionID = binascii.hexlify(os.urandom(50)).decode('ascii')
        cls(
            sessionID=sessionID,
            user=user,
            expiry=timezone.now() + timedelta(days=7)
        ).save()
        return sessionID

    @classmethod
    def delete_old(cls):
        cls.objects.filter(expiry__lte=timezone.now())

    @classmethod
    def get_user(cls, sessionID):
        session = cls.objects.filter(expiry__gt=timezone.now(), sessionID=sessionID).first()
        return None if session is None else session.user
