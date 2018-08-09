from django.contrib import admin

# Register your models here.
from .models import Room, Message

# this allows the admin site to access and edit the room and message models 
admin.site.register(Room)
admin.site.register(Message)