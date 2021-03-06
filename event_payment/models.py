from django.db import models
from django.contrib.auth import get_user_model
from parties.models import Party
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime

# Create your models here.
# Model for bid which inludes bid amount, user (fk) and party pk (int)
class EventPayment(models.Model):
	payment_amount 	= models.DecimalField(max_digits=7, decimal_places=2, default=0)
	payment_user 		= models.ForeignKey(settings.AUTH_USER_MODEL,
					on_delete=models.CASCADE)
	party 		= models.ForeignKey(Party,on_delete=models.CASCADE, null=True, \
		related_name="payment_object")
	is_paid 	= models.BooleanField(default=False)
	task_id			= models.CharField(max_length=50, blank=True, editable=False)
	def __str__(self):
		return str(self.payment_user.username) +" payment for "+str(self.party.title)



	def schedule_pay_owner(self):
		# the pick time is set to be slightly before when the event 
		# actully happens to allow everyone to get set up.
		pay_time = self.party.party_time + timedelta(minutes=1)
		#pay_time = datetime.datetime.now() + timedelta(minutes=1)
		# .astimezone(pytz.utc)
		# brings in the pick winner method
		from .tasks import pay_owner
		result = pay_owner.apply_async((self.pk,), eta=pay_time)
		return result.id
	def save(self, *args, **kwargs):
		# if we've already shceduled it, as in we're editing, cancel it
		if self.task_id:
			celery_app.control.revoke(self.task_id)
		# we call save twice because we have to set the pk before we schedule
		# then we set the task_id as the party id, then we save again
		super(EventPayment, self).save(*args, **kwargs)
		self.task_id = self.schedule_pay_owner()
		# self.send_notifications()	
		self.save2(update_fields=['task_id'])

	def save2(self, *args, **kwargs):
		super(EventPayment, self).save(*args, **kwargs)
# set integrity constraints for database
	def clean(self, *args, **kwargs):
		return super(EventPayment, self).clean(*args,**kwargs)