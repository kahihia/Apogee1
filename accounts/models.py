from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse_lazy

# Create your models here.

# we use this to override the all call
# we want the all call to exclude ourselves
class UserProfileManager(models.Manager):
	# this means that both the user and followed_by have 
	# these methods applied to them
	use_for_related_fields = True

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
	def toggle_follow(self, user, to_toggle_user):
		# this is our own profile
		user_profile, created = UserProfile.objects.get_or_create(user=user)
		# checks to see if the requestuser is already following the toggleuser
		if to_toggle_user in user_profile.following.all():
			user_profile.following.remove(to_toggle_user)
			added = False
		else:
			user_profile.following.add(to_toggle_user)
			added = True
		return added

	# checks if requestuser is following someone
	def is_following(self, user, followed_by_user):
		user_profile, created = UserProfile.objects.get_or_create(user=user)
		if created: # cant be following anyone if the profile was just made
			return False
		if followed_by_user in user_profile.following.all():
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


# this is the profile model. it allows us, through a 
# many to many relationship, to follow people and see 
# who is following us
class UserProfile(models.Model):
	# user.profile gives me my own profile
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

	# this is the same as calling UserProfile.objects.all()
	objects = UserProfileManager()

	def __str__(self):
		return str(self.following.all().count())

	# this is required to eliminate ourselves from our own following lists
	# i think the manager only works on profiles, 
	# and we need to set the following when the actual user is created
	def get_following(self):
		users = self.following.all()
		return users.exclude(username=self.user.username)

	# gets the follow url for the person whose page you are on
	def get_follow_url(self):
		return reverse_lazy('profiles:follow', kwargs={'username': self.user.username})

	# gets the detail view url for a profile
	def get_absolute_url(self):
		return reverse_lazy('profiles:detail', kwargs={'username': self.user.username})


# this signal occurs after the user is saved and ensures that a profile is 
# set up for that user
# it is checking for the created boolean 
def post_save_user_reciever(sender, instance, created, *args, **kwargs):
	if created: 
		new_profile = UserProfile.objects.get_or_create(user=instance)
		# could run celery+redis deferred tasks here like an email task

# sending user object to the receiver
post_save.connect(post_save_user_reciever, sender=settings.AUTH_USER_MODEL)