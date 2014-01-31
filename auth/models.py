from common import models

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
