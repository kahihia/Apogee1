from django.contrib import admin

# Register your models here.
from .models import Bid

# this allows the admin site to access and edit the userprofile model
admin.site.register(Bid)