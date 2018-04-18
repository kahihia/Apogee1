from django.utils.timesince import timeuntil
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from rest_framework import serializers
from django.contrib.auth.models import User

from parties.models import Party 
from accounts.api.serializers import UserDisplaySerializer

class PartyModelSerializer(serializers.ModelSerializer):
	# foreign key relationship to the user serializer
	# would normally display as the id number (from party model), 
	# but serializer allows it to access the data from the user model
	user = UserDisplaySerializer(read_only=True) # cant change user data in create
	# the following three are just converters that give us a readable format
	party_time_display = serializers.SerializerMethodField()
	timeuntil = serializers.SerializerMethodField()
	time_created_display = serializers.SerializerMethodField()
	is_open = serializers.SerializerMethodField()
	stars = serializers.SerializerMethodField()
	did_star = serializers.SerializerMethodField()
	thumbnail_url = serializers.SerializerMethodField()
	short_description = serializers.SerializerMethodField()
	joins = serializers.SerializerMethodField()
	did_join = serializers.SerializerMethodField()
	winner_names = serializers.SerializerMethodField()
	is_owner = serializers.SerializerMethodField()

	class Meta:
		model = Party
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
			'stars',
			'did_star',
			'thumbnail_url',
			'short_description',
			'joins', 
			'did_join',
			'winner_names',
			'is_owner',
			'cost',
		]


	def get_is_owner(self, obj):
		request = self.context.get('request')
		try:
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
		return tz_converted.strftime('%b %d at %I:%M %p')

	def get_timeuntil(self, obj):
		return timeuntil(obj.party_time)

	# this compares the current time to th event time and tells us if it's closed
	def get_is_open(self, obj):
		return timezone.now()<obj.party_time

	def get_time_created_display(self, obj):
		# strftime is python datetime method
		return obj.time_created.strftime('%b %d at %I:%M %p')


