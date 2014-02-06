import re
from django.core.exceptions import ValidationError


def matches_regex(regex, msg, fn=lambda x: x):
    regex = re.compile('^' + regex + '$', re.I)
    def clean_field(self, value):
        value = fn(value)
        if regex.match(value) is None:
            raise ValidationError(msg)
        return value
    return clean_field
