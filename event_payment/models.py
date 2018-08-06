from django.db import models
from django.contrib.auth import get_user_model
from parties.models import Party
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# Create your models here.
# Model for bid which inludes bid amount, user (fk) and party pk (int)
class EventPayment(models.Model):
	payment_amount 	= models.DecimalField(max_digits=7, decimal_places=2, default=0)
	payment_user 		= models.ForeignKey(settings.AUTH_USER_MODEL,
					on_delete=models.CASCADE)
	party 		= models.ForeignKey(Party,on_delete=models.SET_NULL, null=True, \
		related_name="payment_object")
	is_paid 	= models.BooleanField(default=False)
	task_id			= models.CharField(max_length=50, blank=True, editable=False)
	def __str__(self):
		return str(self.payment_user.username) +" payment for "+str(self.party.title)



	def schedule_pay_owner(self):
		print("I am getting scheduled________________________________________________")
		# the pick time is set to be slightly before when the event 
		# actully happens to allow everyone to get set up.
		pay_time = self.party_time + timedelta(minutes=1)
		# .astimezone(pytz.utc)
		# brings in the pick winner method
		from .tasks import pay_owner
		result = pay_owner.apply_async((self.pk,), eta=pick_time)
		return result.id
	def save(self, *args, **kwargs):
		# if we've already shceduled it, as in we're editing, cancel it
		if self.task_id:
			celery_app.control.revoke(self.task_id)
		# we call save twice because we have to set the pk before we schedule
		# then we set the task_id as the party id, then we save again
		super(EventPayment, self).save(*args, **kwargs)
		self.task_id = self.schedule_pick_winner()
		# self.send_notifications()
		super(EventPayment, self).save(*args, **kwargs)

	def save2(self, *args, **kwargs):
		super(Party, self).save(*args, **kwargs)
# set integrity constraints for database
	def clean(self, *args, **kwargs):
		return super(EventPayment, self).clean(*args,**kwargs)