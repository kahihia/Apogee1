# this is the base celery app
# it allows us to call celery processes elsewhere in the app
from __future__ import unicode_literals, absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apogee1.settings.local')

# this just creates an instance for us to use. not what the name matters for
app = Celery('apogee1')

############## This needs to be commented out for local ###############
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))