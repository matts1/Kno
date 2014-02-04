import os
import binascii
from common import models
from django.utils import timezone
from datetime import timedelta
import hashlib

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

    def login(self) -> bytes:
        return Session.create(self)

    @classmethod
    def get(cls, email:str):
        """
        Gets the user that goes by the email given, and returns None if no user is given
        """
        return cls.objects.filter(pk=email).first()

    def __str__(self):
        return self.email

    def pprint(self):
        return self.email

    def __repr__(self):
        return self.email

    def gravatar(self, size):
        # http://en.gravatar.com/site/implement/images/python/
        return '<img src="http://www.gravatar.com/avatar/%s?d=identicon&s=%d" alt="gravatar">' % \
               (hashlib.md5(self.email.lower().encode()).hexdigest(), size)


class Session(models.Model):
    sessionID = models.CharField(max_length=100, primary_key=True, unique=True)
    user = models.ForeignKey(User)
    expiry = models.DateTimeField()

    @classmethod
    def create(cls, user: User) -> bytes:
        sessionid = None
        while sessionid is None or cls.objects.filter(sessionID=sessionid):
            sessionid = binascii.hexlify(os.urandom(50)).decode('ascii')
        cls(
            sessionID=sessionid,
            user=user,
            expiry=timezone.now() + timedelta(days=7)
        ).save()
        return sessionid

    @classmethod
    def delete_old(cls):
        cls.objects.filter(expiry__lte=timezone.now())

    @classmethod
    def get_user(cls, sessionid: str) -> User:
        session = cls.objects.filter(expiry__gt=timezone.now(), sessionID=sessionid).first()
        return None if session is None else session.user
