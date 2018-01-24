from django.utils.timesince import timeuntil
from rest_framework import serializers

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
	stars = serializers.SerializerMethodField()
	did_star = serializers.SerializerMethodField()

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
			'stars',
			'did_star',
		]

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

	def get_stars(self, obj):
		return obj.starred.all().count()

	def get_party_time_display(self, obj):
		# strftime is python datetime method
		return obj.party_time.strftime('%b %d at %I:%M %p')

	def get_timeuntil(self, obj):
		return timeuntil(obj.party_time)

	def get_time_created_display(self, obj):
		# strftime is python datetime method
		return obj.time_created.strftime('%b %d at %I:%M %p')


