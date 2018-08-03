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
	def __str__(self):
		return self.payment_user +" payment for "+self.party



# set integrity constraints for database
	def clean(self, *args, **kwargs):
		return super(EventPayment, self).clean(*args,**kwargs)