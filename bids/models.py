from django.db import models
from parties.models import Party
from django.conf import settings

# Create your models here.
class Bid(models.Model):
	bid_amount 	= models.IntegerField(default = 0)
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL,
					on_delete=models.CASCADE)
	party 		= models.ForeignKey(Party, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.bid_amount)