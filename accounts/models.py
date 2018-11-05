# models are the objects that are actually used and stored in the database
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse_lazy
import random
from notifications.models import Notification
from parties.models import Party
from userstatistics.models import StatisticsInfo
# Create your models here.

class UserProfileManager(models.Manager):
	# this means that both the user and followed_by have 
	# these methods applied to them
	use_for_related_fields = True

	# we use this to override the all call
	# we want the all call to exclude ourselves
	def all(self):
		qs = self.get_queryset().all()
		# self.instance is the user
		try:
			if self.instance:
				qs = qs.exclude(user=self.instance)
		except:
			pass
		return qs

	# changes whether the requestuser is following someone
	# the requestuser is just whoever is doing the clicking
	def toggle_follow(self, user, to_toggle_user):
		# this is our own profile
		# created is just a boolean thats part of th method we're using
		# its not actually used
		user_profile, created = UserProfile.objects.get_or_create(user=user)
		# checks to see if the requestuser is already following the toggleuser
		if to_toggle_user in user_profile.following.all():
			# if they are, remove them from the following list
			user_profile.following.remove(to_toggle_user)
			added = False
		else:
			# if they arent, add them to the following list
			user_profile.following.add(to_toggle_user)
			added = True
		return added

	# changes whether the requestuser is blocking someone
	# the requestuser is just whoever is doing the clicking
	def toggle_block(self, user, to_toggle_user):
		# this is our own profile
		# created is just a boolean thats part of th method we're using
		# its not actually used
		user_profile, created = UserProfile.objects.get_or_create(user=user)
		toggle_user_profile, created2 = UserProfile.objects.get_or_create(user=to_toggle_user)
		# checks to see if the requestuser is already blocking the toggleuser
		if to_toggle_user in user_profile.blocking.all():
			# if they are, remove them from the blocking list
			user_profile.blocking.remove(to_toggle_user)
			added = False
		else:
			# if they arent, add them to the blocking list
			user_profile.blocking.add(to_toggle_user)
			if to_toggle_user in user_profile.following.all():
				user_profile.following.remove(to_toggle_user)
			if user in toggle_user_profile.following.all():
				toggle_user_profile.following.remove(user)
			added = True
		return added

	# checks if requestuser is following someone
	def is_following(self, user, followed_by_user):
		# user is the one we're looking for. self is the request user
		user_profile, created = UserProfile.objects.get_or_create(user=user)
		# created tells us if the user we were searching for exists
		if created: # cant be following anyone if the profile was just made
			return False
		if followed_by_user in user_profile.following.all():
			return True
		return False

	# checks if requestuser is blocking someone
	def is_blocking(self, user, blocked_by_user):
		# user is the one we're looking for. self is the request user
		user_profile, created = UserProfile.objects.get_or_create(user=user)
		# created tells us if the user we were searching for exists
		if created: # cant be blocking anyone if the profile was just made
			return False
		if blocked_by_user in user_profile.blocking.all():
			return True
		return False

	# checks if requestuser is blocked by someone
	def is_blocked(self, user, blocking_user):
		# user is the one we're looking for. self is the request user
		blocking_user_profile, created = UserProfile.objects.get_or_create(user=blocking_user)
		# created tells us if the user we were searching for exists
		if created: # cant be blocking anyone if the profile was just made
			return False
		if blocking_user_profile in user.blocked_by.all():
			return True
		return False

	# this looks at the whole set of users, returns a list of users the requestuser
	# does not follow, ordered randomly
	def recommended(self, user, limit_to=10):
		profile = user.profile
		following = profile.get_following()
		# qs is all profiles not in the users following list and not ourselves
		# the question mark orders it at random
		qs = self.get_queryset().exclude(user__in=following).exclude(id=profile.id).order_by('?')[:limit_to]
		return qs

	# this changes the profiles notifications boolean
	def checked_notifications(self, profile_obj):
		profile_obj.new_notifications = False
		profile_obj.save(update_fields=['new_notifications'])
		return True


# this is the profile model. it allows us, through a 
# many to many relationship, to follow people and see 
# who is following us
class UserProfile(models.Model):
	# user.profile gives me my own profile
	# the .profile calls the related name from the user an grabs the profile obj
	user = models.OneToOneField(
			settings.AUTH_USER_MODEL, 
			on_delete=models.CASCADE, 
			related_name='profile'
		)
	# user.profile.following gives us the users that i follow
	# user.followed_by gives the reverse of following, 
	# which is users that follow me
	following = models.ManyToManyField(
			settings.AUTH_USER_MODEL,
			blank=True, 
			related_name='followed_by'
		)

	# user.profile.blocking gives us the users that i blocked
	# user.blocked_by gives the reverse of blocking, 
	# which is users that have blocked me
	blocking = models.ManyToManyField(
			settings.AUTH_USER_MODEL,
			blank=True, 
			related_name='blocked_by'
		)

	# other fields attatched to users, like their banner, profile pic, bio
	profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', blank=True)

	banner = models.ImageField(upload_to='banners/%Y/%m/%d/', blank=True)	

	bio = models.TextField(max_length=700, blank=True)

	new_notifications = models.BooleanField(default=False)



	email_auth_token	= models.CharField(max_length=6, default="keyaut")
	#To verify important users
	is_verified 		= models.BooleanField(default=False)
	#To authenticate emails
	is_authenticated	= models.BooleanField(default=False)

	account_balance = models.DecimalField(max_digits=12,\
	 							decimal_places=2, default=0)

	twitch_OAuth_token = models.CharField(max_length=100, default="")

	twitch_refresh_token = models.CharField(max_length=100, default="")

	twitch_id = models.CharField(max_length=100, default="")

	# this is the same as calling UserProfile.objects.all()
	# it just connects to the manager
	objects = UserProfileManager()

	# when we print a user, it prints the username
	def __str__(self):
		return str(self.user.username)

	# this is required to eliminate ourselves from our own following lists
	# i think the manager only works on profiles, 
	# and we need to set the following when the actual user is created
	def get_following(self):
		users = self.following.all()
		return users.exclude(username=self.user.username)

	# gets the follow url for the person whose page you are on
	def get_follow_url(self):
		return reverse_lazy('profiles:follow', kwargs={'username': self.user.username})

	def get_twitch_reset_url(self):
		print("less gooooooooooooooooooooooooooooooooooooooooooooo")
		return reverse_lazy('profiles:detwitch', kwargs={'username': self.user.username})

	# gets the follow url for the person whose page you are on
	def get_block_url(self):
		return reverse_lazy('profiles:block', kwargs={'username': self.user.username})

	# gets the detail view url for a profile
	def get_absolute_url(self):
		return reverse_lazy('profiles:detail', kwargs={'username': self.user.username})

	# gets the edit view url for a profile
	def get_edit_url(self):
		return reverse_lazy('profiles:edit', kwargs={'username': self.user.username})

	# gets the total list of events that this user has created
	def event_count(self):
		qs = Party.objects.filter(user=self.user)
		return qs


# this signal occurs after the user is saved and ensures that a profile is 
# set up for that user
# it is checking for the created boolean 
def post_save_user_reciever(sender, instance, created, *args, **kwargs):
	if created: 
		new_profile = UserProfile.objects.get_or_create(user=instance)
		StatisticsInfo.objects.create(user=instance)

		# could run celery+redis deferred tasks here like an email task
		
# this looks for a notification signal and uses the user to set the 
# notifications variable on the appropriate profile
def post_save_has_notification(sender, instance, created, *args, **kwargs):
	if created:
		notif_profile = instance.user.profile
		notif_profile.new_notifications = True
		notif_profile.save(update_fields=['new_notifications'])


# these connect our receivers and set them to listen to the appropriate model
post_save.connect(post_save_user_reciever, sender=settings.AUTH_USER_MODEL)
post_save.connect(post_save_has_notification, sender=Notification)





