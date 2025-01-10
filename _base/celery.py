from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_base.settings")
app = Celery("_base")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Beat schedule of tasks in whole project
app.conf.beat_schedule = {
    "create charge notification": {
        "task": "credit_management.tasks.charge_notification.create_charge_notification",
        "schedule": crontab(minute=30, hour=23),
    },
    "find sellers to notification": {
        "task": "credit_management.tasks.charge_notification.find_sellers_for_notification",
        "schedule": crontab(minute=0, hour=23),
    },
}
