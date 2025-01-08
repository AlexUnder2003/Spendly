from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartsave.settings")
app = Celery("smartsave")
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.conf.imports = ("coins.tasks",)

app.conf.beat_schedule = {
    "test_task_every_10_seconds": {
        "task": "coins.tasks.calculate_daily_balance",
        "schedule": timedelta(seconds=60),  # Каждые 10 секунд
    },
}
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
