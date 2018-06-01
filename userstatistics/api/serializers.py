from django.utils.timesince import timeuntil
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import timedelta

from userstatistics.models import StatisticsInfo 
from accounts.api.serializers import UserDisplaySerializer


class StatisticsInfoModelSerializer(serializers.ModelSerializer):
	user = UserDisplaySerializer(read_only=True) 
	
	class Meta:
		# the API is built on the party model
		model = StatisticsInfo
		# the fields tell us what is in the API. some are Serilaizermethodfields 
		# the others are directly from the model
		fields = [
			'user',
			'max_profit',
		]