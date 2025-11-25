from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]  # cámbialo en producción real

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
