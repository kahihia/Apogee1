from django.contrib import admin

from .models import EventPayment

# this allows the admin site to access and edit the userprofile model
admin.site.register(EventPayment)
