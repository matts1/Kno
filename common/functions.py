import os
import binascii


def genunique(model, attr, length):
    length //= 2
    val = binascii.hexlify(os.urandom(length)).decode('ascii')
    while model.objects.filter(**{attr: val}):
        val = binascii.hexlify(os.urandom(length)).decode('ascii')
    return val
