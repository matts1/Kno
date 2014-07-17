from auth.models import User
from common import models


class Notification(models.Model):
    heading = models.TextField(max_length=100)
    text = models.TextField(max_length=200)
    url = models.URLField()
    users = models.ManyToManyField(User, related_name='notifications')

    @classmethod
    def create(cls, users, heading, text, url):
        notif = Notification(heading=heading, text=text, url=url)
        notif.save()  # need to save it first, otherwise I can't modify the users
        if not isinstance(users, list):
            users = users.all()
        notif.users.add(*users)
        notif.save()
