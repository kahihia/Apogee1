from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import UserProfile

# Create your tests here.
User = get_user_model()

class UserProfileTestCase(TestCase):
	# this ensures that the profile created has the right info
	def setUp(self):
		self.username = 'some_user'
		new_user = User.objects.create(username=self.username)

	# ensures the profile is the only thing created
	def test_profile_created(self):
		username = self.username
		user_profile = UserProfile.objects.filter(user__username=self.username)
		self.assertTrue(user_profile.exists())
		self.assertTrue(user_profile.count() == 1)

