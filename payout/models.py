from django.db import models
from django.conf import settings

class Payout(models.Model):
	# Create your models here.
	payout_user 		= models.ForeignKey(
							settings.AUTH_USER_MODEL, 
							on_delete=models.CASCADE
						)
	payout_amount 		= models.DecimalField(max_digits=12, decimal_places=2, default=0)
	time_requested		= models.DateTimeField(auto_now_add=True)
	description 		= models.CharField(max_length=280)
	payment_info		= models.CharField(max_length=40)
	is_paid 			= models.BooleanField(default=False)