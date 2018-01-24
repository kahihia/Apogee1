from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Party

# Create your tests here.

User = get_user_model()

class PartyModelTestCase(TestCase):
	def setUp(self):
		random_user = User.objects.create(username='TheC27')

	def test_party_item(self):
		obj = Party.objects.create(
				user=User.objects.first(),
				title='A random title', 
				description='A random description', 
				party_time='2018-01-24 16:00'
			)
		self.assertTrue(obj.title == 'A random title')
		self.assertTrue(obj.description == 'A random description')
		self.assertTrue(obj.id == 1)
		absolute_url = reverse('parties:detail', kwargs={'pk': 1})
		self.assertEqual(obj.get_absolute_url(), absolute_url)

	def test_tweet_url(self):
		obj = Party.objects.create(
				user=User.objects.first(),
				title='A random title', 
				description='A random description', 
				party_time='2018-01-24 16:00'
			)
		absolute_url = reverse('parties:detail', kwargs={'pk': obj.pk})
		self.assertEqual(obj.get_absolute_url(), absolute_url)