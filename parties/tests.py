# these methods test the party model itself
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Party

# Create your tests here.

# we're using the user model because each party has an associated user
User = get_user_model()

class PartyModelTestCase(TestCase):
	# this created a user object for us to test with
	def setUp(self):
		random_user = User.objects.create(username='TheC27')

	# this tests that the event creates properly
	def test_party_item(self):
		# this creates the event we can check
		obj = Party.objects.create(
				user=User.objects.first(),
				title='A random title', 
				description='A random description', 
				party_time='2018-01-24 16:00'
			)
		# assert true actually checks each piece and throws a failure if it doesnt pass
		self.assertTrue(obj.title == 'A random title')
		self.assertTrue(obj.description == 'A random description')
		self.assertTrue(obj.id == 1)
		# this cchecks that the url routes to the correct event
		absolute_url = reverse('parties:detail', kwargs={'pk': 1})
		self.assertEqual(obj.get_absolute_url(), absolute_url)

	# this jsut checks the URL. its a duplicate
	def test_party_url(self):
		obj = Party.objects.create(
				user=User.objects.first(),
				title='A random title', 
				description='A random description', 
				party_time='2018-01-24 16:00'
			)
		absolute_url = reverse('parties:detail', kwargs={'pk': obj.pk})
		self.assertEqual(obj.get_absolute_url(), absolute_url)