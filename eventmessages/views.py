from django.shortcuts import render
import logging
from .models import Room
import json

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'chat/index.html', {})

# Create your views here.
def chat_room(request, label):
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room, created = Room.objects.get_or_create(label=label)
    logger.debug("Rooms, created " + room.name)
    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })