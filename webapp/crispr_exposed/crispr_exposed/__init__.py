from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that (shared_)task will use this app.
from .celery import app as celery_app  # noqa   ##should be commented for running manage.py celery
