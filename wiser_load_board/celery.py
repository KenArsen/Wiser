from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiser_load_board.settings")
app = Celery("wiser_load_board")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "my_periodic_task": {
        "task": "apps.order.tasks.process_and_save_emails_task",
        "schedule": timedelta(seconds=3),
    },
    "delete_expired_data": {
        "task": "apps.order.tasks.delete_expired_data",
        "schedule": timedelta(minutes=3),
    },
    "get_location": {
        "task": "apps.order.location_tasks.get_location",
        "schedule": timedelta(minutes=5),
    },
}
