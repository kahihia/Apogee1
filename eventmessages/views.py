from django.shortcuts import render
import logging
from .models import Room, Message
import json

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'chat/index.html', {})
