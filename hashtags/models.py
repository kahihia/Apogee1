from django.db import models
from django.db.models import Q
from django.urls import reverse_lazy

# Create your models here.
from parties.models import Party
from .signals import parsed_hashtags

# this is the actual hashtag object that we use. they're embedded 
# within party objects
class HashTag(models.Model):
	# this is the only data associated with the tags. its the text and a time
	tag = models.CharField(max_length=140)
	time_created = models.DateTimeField(auto_now_add=True)

	# this just tells us how it will render when we try to display the object
	def __str__(self):
		return self.tag

	# this gives us the routing for when we click a hashtag
	def get_absolute_url(self):
		return reverse_lazy('hashtag', kwargs={'hashtag': self.tag})

	# this gets a list of the parties that contain the tag 
	# in their title or their description
	# i think this is a duplicate since the API is what is actually 
	# handling the search for us
	def get_parties(self):
		return Party.objects.filter(
				Q(title__icontains='#' + self.tag) | 
				Q(description__icontains='#' + self.tag)
			)


# creates the hashtags when the event is created, not on first click
# this relates to the signals file in this folder 
def parsed_hashtags_receiver(sender, hashtag_list, *args, **kwargs):
	if len(hashtag_list) > 0:
		for tag_var in hashtag_list:
			new_tag, created = HashTag.objects.get_or_create(tag=tag_var)


parsed_hashtags.connect(parsed_hashtags_receiver)







