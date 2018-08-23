from django.db import models
from django.utils import timezone

# Create your models here.
class Room(models.Model):
    name = models.TextField()

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete='cascade')
    message = models.TextField()
    username = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)