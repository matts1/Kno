import os
import binascii


def genunique(model, attr, length):
    length //= 2
    val = binascii.hexlify(os.urandom(length)).decode('ascii')
    while model.objects.filter(**{attr: val}):
        val = binascii.hexlify(os.urandom(length)).decode('ascii')
    return val


BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')
def makepath(x):
    return os.path.join(BASE_DIR, x)
