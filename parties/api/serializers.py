# serializers tell us what info from the model is visible in the API
from django.utils.timesince import timeuntil
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from rest_framework import serializers
from django.contrib.auth.models import User

from parties.models import Party 
# we import the user serializer as well since the event 
# serializer displays user info as well
from accounts.api.serializers import UserDisplaySerializer

class PartyModelSerializer(serializers.ModelSerializer):
	# foreign key relationship to the user serializer
	# would normally display as the id number (from party model), 
	# but serializer allows it to access the data from the user model
	# the readonly just means that you cant edit a user from an event
	user = UserDisplaySerializer(read_only=True) 
	# this is a prettier display for the time that converts to AM/PM
	party_time_display = serializers.SerializerMethodField()
	# time until the event time
	timeuntil = serializers.SerializerMethodField()
	# prettier AM/PM display for time created. currently unused
	time_created_display = serializers.SerializerMethodField()
	# tells us if the event time has passed or not
	is_open = serializers.SerializerMethodField()
	# how many people have starred the event
	stars = serializers.SerializerMethodField()
	# tells us if the requestuser has starred this one. 
	did_star = serializers.SerializerMethodField()
	# routes to the thumbnail in the media folder. 
	thumbnail_url = serializers.SerializerMethodField()
	# this is a shortened version of the description that fits the thumbnail
	short_description = serializers.SerializerMethodField()
	# numberof people that have joined the event
	joins = serializers.SerializerMethodField()
	# tells us if the requestuser has joined the event
	did_join = serializers.SerializerMethodField()
	# this hold the list of winning users after the event has closed
	winner_names = serializers.SerializerMethodField()
	# tells us if requestuser was the one who created this event. 
	is_owner = serializers.SerializerMethodField()

	class Meta:
		# the API is built on the party model
		model = Party
		# the fields tell us what is in the API. some are Serilaizermethodfields 
		# the others are directly from the model
		fields = [
			'id',
			'user', 
			'title', 
			'description', 
			'party_time', 
			'time_created', 
			'party_time_display',
			'timeuntil',
			'time_created_display', 
			'is_open',
			'event_type', 
			'stars',
			'did_star',
			'thumbnail_url',
			'short_description',
			'joins', 
			'did_join',
			'winner_names',
			'is_owner',
			'cost',
			'num_winners',
		]

	# method if you want the human readable format of the event type
	# def get_readable_event_type(self, obj):
	# 	return obj.get_event_type_display()


	# The methods below define the SerializerMethodFields
	def get_is_owner(self, obj):
		request = self.context.get('request')
		try:
			# actually checks the event user versus the request
			user = request.user
			if user.is_authenticated:
				if user == obj.user:
					return True
		except:
			pass
		return False

	# we use winner names because the winner list itself just contains the primary keys
	def get_winner_names(self, obj):
		names = []
		w = obj.winners.all()
		for user in w:
			names.append(user.username)
		return names

	# this limits the characters for displaying on the thumbnail
	def get_short_description(self, obj):
		return truncatechars(obj.description, 40)

	def get_thumbnail_url(self, obj):
		return obj.thumbnail.url

	# requires try block because it may throw an error
	def get_did_star(self, obj):
		request = self.context.get('request')
		try: 
			user = request.user
			if user.is_authenticated:
				if user in obj.starred.all():
					return True
		except:
			pass
		return False

	def get_did_join(self, obj):
		request = self.context.get('request')
		try: 
			user = request.user
			if user.is_authenticated:
				if user in obj.joined.all():
					return True
		except:
			pass
		return False

	def get_stars(self, obj):
		return obj.starred.all().count()

	def get_joins(self, obj):
		return obj.joined.all().count()

	def get_party_time_display(self, obj):
		# strftime is python datetime method. the localtime call 
		# converts it back to the local time because it is converted 
		# to UTC when it's stored in the database
		tz_converted = timezone.localtime(obj.party_time)
		# the % is just formatting
		return tz_converted.strftime('%b %d at %I:%M %p')

	def get_timeuntil(self, obj):
		return timeuntil(obj.party_time)

	# this compares the current time to the event time and tells us if it's closed
	def get_is_open(self, obj):
		return timezone.now()<obj.party_time

	def get_time_created_display(self, obj):
		# strftime is python datetime method
		return obj.time_created.strftime('%b %d at %I:%M %p')


