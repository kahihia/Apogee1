from django.contrib import admin

# Register your models here.
from .models import HashTag

# this just makes it so we can access tags in the admin
admin.site.register(HashTag)