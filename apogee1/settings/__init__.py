from __future__ import unicode_literals, absolute_import
# this allows the setting folder to look like a module
# we do this because we have multiple settings

# base is loaded first
from .base import *

# # production will override base
# from .production import *

# # local will override production and base
# # not sure why it's in a try block
# try:
# 	from .local import *
# except:
# 	pass

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ['celery_app']