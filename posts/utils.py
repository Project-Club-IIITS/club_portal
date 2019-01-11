import pyffx
from django.conf import settings

encrypter = pyffx.Integer(settings.SECRET_KEY.encode('UTF-8'), length=settings.POST_ID_SECRET_LENGTH)


def encrypt_id(id):
    return encrypter.encrypt(id)


def decrypt_id(enc_id):
    return encrypter.decrypt(enc_id)
