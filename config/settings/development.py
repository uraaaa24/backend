from .base import *

DATABASE = {
  "default": {
    "ENGINE": "django.db.backends.mysql",
    "NAME": "app",
    "USER": "root",
    "PASSWORD": "password",
    "HOST": "host.docker.internal",
    "PORT": "53306",
    "ATOMIC_REQUESTS": True
  }
}
