from django.contrib import admin

from .models import StatisticsInfo

# this allows the admin site to access and edit the userprofile model
admin.site.register(StatisticsInfo)
