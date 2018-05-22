# this handles the data associated with parties 
import re
import pytz
from django.db.models import F
from datetime import timedelta
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from bids.models import Bid
from .validators import validate_title
from hashtags.signals import parsed_hashtags
from apogee1.settings import celery_app

# Create your models here.

# the manager creates additional methods the objects can use
class PartyManager(models.Manager):
	# this both adds or removes the user and tells us if they're on it
	def star_toggle(self, user, party_obj):
		if user in party_obj.starred.all():
			is_starred = False
			party_obj.starred.remove(user)
		else:
			is_starred = True
			party_obj.starred.add(user)
		return is_starred

	# this isnt really a toggle. once you've been added, it sticks
	def join_toggle(self, user, party_obj):
		if not party_obj.is_open:
			won = False
		elif user in party_obj.joined.all():
			is_joined = True
		else:
			is_joined = True
			party_obj.joined.add(user)
		return is_joined

	def buyout_toggle(self, user, party_obj):
		hold_val = party_obj.num_curr_winners
		if not party_obj.is_open:
			won = False
		elif user in party_obj.winners.all():
			won=True

		elif party_obj.num_curr_winners>=party_obj.num_possible_winners:
			won = False
		else:
			party_obj.num_curr_winners =F('num_curr_winners') + 1
			party_obj.winners.add(user)
			hold_val = hold_val+1
			print(party_obj.num_curr_winners)
			print("<")
			print(party_obj.num_possible_winners)
			if hold_val==party_obj.num_possible_winners:
				print("Closing party object")
				party_obj.is_open = False
			won= True
			party_obj.save()
		return won

	def bid_toggle(self, user, party_obj, bid):
		print("First for loop")
		party_num_curr_winners = party_obj.num_curr_winners
		party_num_possible_winners = party_obj.num_possible_winners
		bid_list = Bid.objects.filter(party=party_obj.pk)
		for b in bid_list:
			print("USER: "+str(b.user)+"  AMOUNT: "+str(b.bid_amount)+" PARTY: "+str(b.party))
		print("end for loop")
		print(1)
		if not party_obj.is_open:
			won = False 
		elif user in party_obj.joined.all():
			print(2)
			print("User already in bid_list")
			bid_accepted = False
		elif party_obj.num_curr_winners<party_obj.num_possible_winners:
			print(3)
			party_obj.num_curr_winners = F('num_curr_winners') + 1
			party_obj.joined.add(user)
			new_bid = Bid.objects.create(user=user, party=party_obj.pk, bid_amount=bid)
			print("New bid is: "+str(new_bid.bid_amount)+" by "+str(new_bid.user)+" from open slot")
			bid_accepted = True
			if party_num_curr_winners+1==party_num_possible_winners:
				min_bid = bid_list.first()
				for bs in bid_list:
					if min_bid.bid_amount>bs.bid_amount:
						min_bid=bs
				party_obj.minimum_bid = min_bid.bid_amount		
			new_bid.save()
			party_obj.save()
		else:
			print(4)
			min_bid = bid_list.first()
			for bids in bid_list:
				if min_bid.bid_amount>bids.bid_amount:
					min_bid=bids
			if min_bid.bid_amount<bid:
				print("Removing smallest bid by: "+str(min_bid.user))
				Bid.objects.filter(pk=min_bid.pk).delete()
				party_obj.joined.remove(min_bid.user)
				party_obj.joined.add(user)

				new_bid = Bid.objects.create(user=user, party=party_obj.pk, bid_amount=bid)
				print("New bid is: "+str(new_bid.bid_amount)+" by "+str(new_bid.user)+" from winning slot")
				blist = Bid.objects.filter(party=party_obj.pk)
				min_bid = blist.first()
				for bs in blist:
					print("This is what I am talking about: "+str(bs.bid_amount))
					if min_bid.bid_amount>bs.bid_amount:
						min_bid=bs
				party_obj.minimum_bid = min_bid.bid_amount
				bid_accepted=True
				party_obj.save()
				new_bid.save()

			else:
				party_obj.minimum_bid = min_bid.bid_amount
				print("party min bid is: "+str(party_obj.minimum_bid))
				print("Bid not large enough to usurp other")
				bid_accepted=False
				party_obj.save()

		print(5)			
		return bid_accepted


	# this isnt really a toggle. once you've been added, it sticks
	def win_toggle(self, user, party_obj):
		if user in party_obj.winners.all():
			won = True

		else:
			won = True
			party_obj.winners.add(user)
		return won

	# this was misnamed. starred by generally refers to the list of things that 
	# def get_starred_by(self, user, party_obj):
	# 	return party_obj.starred.all()


# this is the actual model that stores all the data
class Party(models.Model):
	# this links each event to a user object
	user 			= models.ForeignKey(
						settings.AUTH_USER_MODEL, 
						on_delete=models.CASCADE
					)
	title 			= models.CharField(
						max_length=140, 
						validators=[validate_title]
					)
	description 	= models.CharField(max_length=280)
	# auto_now_add automatically inputs the current time on creation
	time_created	= models.DateTimeField(auto_now_add=True)
	# auto_now adds the time, but it can be overwritten if it adds again
	updated 		= models.DateTimeField(auto_now=True)
	party_time		= models.DateTimeField()

	minimum_bid		= models.IntegerField(default=0)

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
	#Number of possible winners - sepcified by the creator on event creation
	num_possible_winners = models.PositiveSmallIntegerField(default=1)
	#Number of current winners, incremented each time a winner is added to winners list
	num_curr_winners = models.PositiveSmallIntegerField(default=0)
	# The maximum number of entrants to a lottery event. not required, defaults to no limit
	max_entrants = models.PositiveSmallIntegerField(blank=True, null=True, 
													choices=(
														(None, 'Unlimited'), 
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

	thumbnail 		= models.ImageField(upload_to='thumbnails/%Y/%m/%d/') 
	# task_id is the celery identifier, used to make sure that we don't 
	# duplicate picking winners
	task_id			= models.CharField(max_length=50, blank=True, editable=False)

	cost 			= models.DecimalField(max_digits=7, decimal_places=2, default=0)


	# declares our choices for event types
	event_type		= models.IntegerField(
						choices=(
							(1, 'Drawing'), 
							(2, 'Bid'), 
							(3, 'Buy')),  
						default=1)

	# durationField for when to close it relative to the event time
	# use small integerfield for event type? map 1 to lottery, 2 to buy, 3 to bid?

	# this just allows the party objects to use the manager methods
	objects = PartyManager()
	
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
		self.task_id = self.schedule_pick_winner()
		super(Party, self).save(*args, **kwargs)

	def get_min_bid(self):
		bid_list = self.bid_list

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







