# serializers tell us what info from the model is visible in the API
from django.utils.timesince import timeuntil
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import timedelta

from eventmessages.models import Message 
# we import the user serializer as well since the event 
# serializer displays user info as well
from decouple import config

class MessageModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Message
		fields = [
			'id',
			'room', 
			'username', 
			'message', 
			'timestamp'
		]