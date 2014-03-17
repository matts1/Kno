from django.conf import settings
from django.core.urlresolvers import reverse
from common import models
from django.utils import timezone
from datetime import timedelta
import hashlib
import smtplib
from common.functions import genunique

SCHOOLS = (
    ('chs', 'Chatswood High School'),
)

class User(models.Model):
    email = models.EmailField(max_length=100, unique=True,
                              error_messages={'unique': 'The email address is already taken'})
    pwd = models.CharField('Password', max_length=128)
    fname = models.CharField('First Name', max_length=50)
    lname = models.CharField('Last Name', max_length=50, )
    reset_code = models.CharField(max_length=100, default=None, blank=True, null=True)
    school = models.CharField(max_length=50, choices=SCHOOLS, default='chs')

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
        return cls.objects.filter(email=email).first()

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

    def forgotpwd(self):
        self.reset_code = genunique(User, 'reset_code', 100)
        self.save()
        self.send_mail(
            'Password Reset',
            ('A password reset has been requested for {name} on http://{site}.\n'
            'If you did not request the reset, don\'t worry, your account is still secure.\n\n'
            'To reset your password go to the following URL.\n'
            'http://{site}{url}').format(
                name=self.get_full_name(),
                site=settings.WEBSITE_URL,
                url=reverse('doresetpwdview', args=(str(self.reset_code),))
            )
        )

    def send_mail(self, subject, body):
        sender='support@%s' % settings.WEBSITE_URL
        msg = ('From: Kno support <%s>\n'
                'To: %s %s <%s>\n'
                'Subject: Kno - %s\n'
                'Dear %s\n\n%s\n\n'
                'Please contact us if you have any questions\n\n'
                'Kno'
                 % (sender, self.fname, self.lname, self.email, subject, self.fname, body)
        )
        if settings.DEBUG:
            print(msg)
        else:
            if not settings.TEST:
                smtpObj = smtplib.SMTP('localhost')
                smtpObj.sendmail(sender, self.email, msg)

    def get_courses_taught(self):
        from courses.models import Course  # 2 way import
        return Course.objects.filter(teacher=self)

    def can_interact(self, data, table):
        cls_name = table.__name__
        if cls_name == 'User':
            return True
        elif cls_name == 'Course':
            return data.teacher == self or data.students.filter(email=self.email).first() is not None
        elif cls_name == 'Task':
            from courses.models import Course  # bidirectional import
            return self.can_interact(data.course, Course)
        else:
            raise NotImplementedError

class Session(models.Model):
    sessionID = models.CharField(max_length=100, primary_key=True, unique=True)
    user = models.ForeignKey(User)
    expiry = models.DateTimeField()

    @classmethod
    def create(cls, user: User) -> bytes:
        sessionid = None
        while sessionid is None or cls.objects.filter(sessionID=sessionid):
            sessionid = genunique(Session, 'sessionID', 100)
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

    def __repr__(self):
        return 'Session for {} starting with {}'.format(self.user, self.sessionID[:10])
