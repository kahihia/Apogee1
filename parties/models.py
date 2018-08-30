# this handles the data associated with parties 
import re
import pytz
from django.db.models import F
from datetime import timedelta, datetime
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from profanity.validators import validate_is_profane
import math
import sys
#from event_payment import partyTransactions
from .validators import validate_title
from hashtags.signals import parsed_hashtags
from apogee1.settings import celery_app
import os
from uuid import uuid4

def path_and_rename(instance, filename):
    upload_to = 'photos'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)



# this is the actual model that stores all the data
class Party(models.Model):
	# this links each event to a user object
	user 			= models.ForeignKey(
						settings.AUTH_USER_MODEL, 
						on_delete=models.CASCADE
					)
	title 			= models.CharField(
						max_length=140, 
						validators=[validate_title, validate_is_profane])
	description 	= models.CharField(max_length=280, validators=[validate_is_profane])
	# auto_now_add automatically inputs the current time on creation
	time_created	= models.DateTimeField(auto_now_add=True)
	# auto_now adds the time, but it can be overwritten if it adds again
	updated 		= models.DateTimeField(auto_now=True)
	party_time		= models.DateTimeField()

	minimum_bid		= models.DecimalField(max_digits=7, decimal_places=2, default=0)
	interaction_pts	= models.IntegerField(default=0)
	time_pts		= models.DecimalField(default=0, max_digits=10, decimal_places=4)
	popularity		= models.DecimalField(default=0, max_digits=10, decimal_places=4)

	# starred contains the users that have starred the event. that means that
	# starred_by should include all the events that a user has starred
	starred 		= models.ManyToManyField(
						settings.AUTH_USER_MODEL, 
						blank=True, 
						related_name='starred_by'
					)
	# joined contains the users that have joined the event. that means that
	# joined_by includes all the events that a user has joined
	joined 			= models.ManyToManyField(
						settings.AUTH_USER_MODEL, 
						blank=True, 
						related_name='joined_by'
					)
	# winners contains the joined users that have been randomly selected
	# won_by includes all the events a user has won
	winners  		= models.ManyToManyField(
						settings.AUTH_USER_MODEL, 
						blank=True, 
						related_name='won_by'
					)
	report_list 	= models.ManyToManyField(
						settings.AUTH_USER_MODEL, 
						blank=True, 
						related_name='reported_by'
					)
	is_flagged 		= models.BooleanField(default=False)
	#Number of possible winners - sepcified by the creator on event creation
	num_possible_winners = models.PositiveSmallIntegerField(default=1)
	#Number of current winners, incremented each time a winner is added to winners list
	#num_curr_winners = models.PositiveSmallIntegerField(default=0)
	# The maximum number of entrants to a lottery event. not required, defaults to no limit
	max_entrants = models.PositiveSmallIntegerField(blank=True, null=True, 
													choices=(
														(None, 'Unlimited'), 
														(3, 3),
														(10, 10), 
														(25, 25), 
														(50, 50), 
														(100, 100), 
														(500, 500), 
														(1000, 1000)))
	#is_open refers to whether the event has closed either
	# due to time ending or max cap being reached
	is_open = models.BooleanField(default=True)

	#highest_bid = models.PositiveSmallIntegerField(default = 0)
	thumbnail 		= models.ImageField(upload_to=path_and_rename, max_length=255, null=True, blank=True)
	#thumbnail 		= models.ImageField(upload_to='thumbnails/%Y/%m/%d/') 
	# task_id is the celery identifier, used to make sure that we don't 
	# duplicate picking winners
	task_id			= models.CharField(max_length=50, blank=True, editable=False)

	cost 			= models.DecimalField(max_digits=7, decimal_places=2, default=0)


	# declares our choices for event types
	event_type		= models.IntegerField(
						choices=(
							(1, 'Lottery'), 
							(2, 'Bid'), 
							(3, 'Buy')),  
						default=1)

	
	# this is what success_url reroutes to if it is not defined in the view
	def get_absolute_url(self):
		return reverse('parties:detail', kwargs={'pk':self.pk})

	# this names it for the database. any time you print the object, the title 
	# is what prints
	def __str__(self):
		return str(self.title) 

	# this calls our celery task to get a winner
	def schedule_pick_winner(self):
		# the pick time is set to be slightly before when the event 
		# actully happens to allow everyone to get set up.
		pick_time = self.party_time - timedelta(minutes=10)
		# .astimezone(pytz.utc)
		# brings in the pick winner method
		from .tasks import pick_winner
		result = pick_winner.apply_async((self.pk,), eta=pick_time)
		return result.id

	# sets our time point offset on creation
	def set_time_pts(self):
		epoch = datetime(2018, 1, 1, 0, 0).astimezone(pytz.utc)
		td = self.time_created - epoch
		seconds = td.total_seconds()
		return seconds/45000

	# @periodic_task(
 #    	run_every=(crontab(minute='*/1')),
 #    	name="decay_popularity",
 #    	ignore_result=True
	# )
	# def task_decay_popularity(self):
	# 	decay_rate =.03
	# 	self.popularity = F('popularity') * (1-decay_rate)
	# 	self.save2(update_fields=['popularity'])


	# def send_notifications(self):
	# 	pick_time = self.party_time - timedelta(minutes=9)
	# 	from .tasks import  send_end_notifications
	# 	success =  send_end_notifications.apply_async((self.pk,), eta=pick_time)
	# 	return success
	# @app.on_after_configure.connect
	# def setup_periodic_popularity_decay(self):
	# 	decay_time = timedelta(minutes=15)
	# 	from .tasks import decay_popularity
	# 	decay_popularity.add_periodic_task(450.0,)
	# 	if self.is_open:

	# used to change the dataset ordering
	class Meta:
		ordering = ['-time_created']

	# overrides the save method to make sure pick_winner is scheduled
	def save(self, *args, **kwargs):
		# if we've already shceduled it, as in we're editing, cancel it
		if self.task_id:
			celery_app.control.revoke(self.task_id)
		# we call save twice because we have to set the pk before we schedule
		# then we set the task_id as the party id, then we save again
		super(Party, self).save(*args, **kwargs)
		self.minimum_bid = self.cost
		self.time_pts = self.set_time_pts()
		self.task_id = self.schedule_pick_winner()
		# self.send_notifications()
		super(Party, self).save(*args, **kwargs)

	def save2(self, *args, **kwargs):
		super(Party, self).save(*args, **kwargs)

	# this validation is called anytime you save a model
	# def clean(self, *args, **kwargs):
	# 	title = self.title
	# 	if title == 'poop':
	# 		raise ValidationError('Title cannot be poop')
	# 	return super(Party, self).clean(*args, **kwargs)

# could use a post save to parse through the title and description to 
# pull out the hashtags and create them in the database

# this would be how you add a notification system
# it enacts certain methods on saving an event
def party_save_receiver(sender, instance, created, *args, **kwargs):
	if created:
		# this looks for usernames in event desctriptions to highlight them
		# and potentially send a notification
		user_regex = r'@(?P<username>[\w.@+-]+)'
		usernames = re.findall(user_regex, instance.description)
		# send notification here

		# this finds hashtags and actually sends the signal to create them 
		# in the hashtag app.
		hash_regex = r'#(?P<hashtag>[\w/d-]+)'
		hashtags = re.findall(hash_regex, instance.description)
		# this sends the list over to the hashtags app so that they can be created
		parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)
		#send hashtag signal here


post_save.connect(party_save_receiver, sender=Party)

@receiver(pre_delete, sender=Party)
def return_funds(sender, instance, **kwargs):
	party_obj = instance
	if party_obj.event_type==1:
		user_list = party_obj.joined.all()
		for user in user_list:
			curr_balance = user.profile.account_balance + party_obj.cost
			user.profile.account_balance = curr_balance
			user.profile.save(update_fields=['account_balance'])
	elif party_obj.event_type==2:
		a=5
	else:
		user_list = party_obj.winners.all()
		for user in user_list:
			curr_balance = user.profile.account_balance + party_obj.cost
			user.profile.account_balance = curr_balance
			user.profile.save(update_fields=['account_balance'])
