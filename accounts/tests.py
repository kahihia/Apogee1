from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import UserProfile

# Create your tests here.
# this gathers the user model for us to test on 
User = get_user_model()

class UserProfileTestCase(TestCase):
	# this ensures that the profile created has the right info

	# setup makes us a profile in a the test database for us to test on
	def setUp(self):
		self.username = 'some_user'
		new_user = User.objects.create(username=self.username)

	# ensures the profile is the only thing created
	def test_profile_created(self):
		username = self.username #declared above
		# we're searching for the one we created above
		user_profile = UserProfile.objects.filter(user__username=self.username)
		# checks if the profile we made is there
		self.assertTrue(user_profile.exists())
		# checks if that profile is the only one made 
		self.assertTrue(user_profile.count() == 1)

