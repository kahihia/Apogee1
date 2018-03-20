from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import serializers

User = get_user_model()

# serializes the user data so that it is api readable
class UserDisplaySerializer(serializers.ModelSerializer):
	# this is called a method field, used to show better data
	# in a form that isnt readily available on the user model itself
	url = serializers.SerializerMethodField()
	class Meta:
		model = User
		# we name the fields here because we dont want to put all the info, like password
		# on the api
		fields = [
			'username', 
			'first_name', 
			'last_name', 
			'url'
			# 'email'
		]

	def get_url(self, obj):
		return reverse_lazy('profiles:detail', kwargs={'username': obj.username})