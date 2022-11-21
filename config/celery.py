import os

from celery import Celery

from config.settings.base import ENVIRONMENT

os.environ.setdefault("DJANGO_SETTINGS_MODULE", ENVIRONMENT)

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
