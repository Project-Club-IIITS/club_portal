import os

IS_PUBLIC = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'bm+!!um=2p&r^!4(l5bpic2f&a7h0!vk^zl$53@drcuvaps08+'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'adwaitthatteytemp@gmail.com'
EMAIL_HOST_PASSWORD = "Ask Adwait Yourself"

POST_ID_SECRET_LENGTH = 6

CREDENTIAL_CERTIFICATE_PATH = os.path.join(BASE_DIR, 'club_portal', 'fake_certificate.json')