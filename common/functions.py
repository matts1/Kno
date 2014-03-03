import os
import binascii

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')


def genunique(model, attr, length):
    length //= 2  # generates length bytes, which is 2*length hex numbers
    val = binascii.hexlify(os.urandom(length)).decode('ascii')
    while model.objects.filter(**{attr: val}):
        val = binascii.hexlify(os.urandom(length)).decode('ascii')
    return val


def makepath(x):
    return os.path.join(BASE_DIR, x)
