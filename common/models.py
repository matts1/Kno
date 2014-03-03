from django.db.models import *

class Model(Model):
    def full_clean(self, exclude=None, validate_unique=True):
        return super().full_clean(exclude, True)

    class Meta:
        abstract = True
