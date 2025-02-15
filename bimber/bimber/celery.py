import os

import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bimber.settings')

app = celery.Celery('bimber')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.timezone = settings.TIME_ZONE
app.conf.broker_connection_retry_on_startup = True
