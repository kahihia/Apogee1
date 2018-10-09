from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import serializers

User = get_user_model()

# This serializer determines the data that is readable off of the 
# user API. Directly displaying the users would make passwords
# available, so we have to explicitly name what data is available.
class UserDisplaySerializer(serializers.ModelSerializer):
	# MethodFields declare API fields that either aren't part of the model or 
	# need to be reformatted for display
	url = serializers.SerializerMethodField()
	is_verified = serializers.SerializerMethodField()
	profile_picture = serializers.SerializerMethodField()
	is_authenticated = serializers.SerializerMethodField()
	class Meta:
		model = User
		# Fields eplicitly states the data and names that are available
		# in the API
		fields = [
			'id',
			'username', 
			'first_name', 
			'last_name', 
			'url',
			'is_verified',
			'is_authenticated'
			'profile_picture',
			# 'email'
		]

	# Anything that is a MethodField needs a get method
	# the data either needs to be found or altered from the model format
	def get_url(self, obj):
		# reverse_lazy brings back a url to the named page "profiles:detail"
		# the kwargs just provides the information required
		return reverse_lazy('profiles:detail', kwargs={'username': obj.username})

	def get_is_verified(self, obj):
		return obj.profile.is_verified	

	def get_has_valid_email(self,obj):
		return obj.profile.is_authenticated

	def get_profile_picture(self, obj):
		if obj.profile.profile_picture and hasattr(obj.profile.profile_picture, 'url'):
			return obj.profile.profile_picture.url
		else:
			return None