from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from parties.models import Party

from .validators import validate_bid_amount
User = get_user_model()


# Model for bid which inludes bid amount, user (fk) and party (fk)
class Bid(models.Model):
	bid_amount 	= models.IntegerField(default = 0, validators = [validate_bid_amount])
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL,
					on_delete=models.CASCADE)
	party 		= models.ForeignKey(Party, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.bid_amount)

# set integrity constraints for database
	def clean(self, *args, **kwargs):
		# bid_amount = self.bid_amount
		# user = self.user
		# party = self.party

		# #bid can't be less than 0
		# if bid_amount<0:
		#  	raise ValidationError("CONTENT ERROR: Cannot be less than 0")
		# #if the user does not exist, bid can't be created	
		# if not User.objects.filter(id = user.id).exists():
		# 	raise ValidationError("CONTENT ERROR: User does not exist")
		# #if the party does not exist, bid can't be created	
		# if not Party.objects.filter(id = party.id).exists():
		# 	raise ValidationError("CONTENT ERROR: Party does not exist")
		return super(Bid, self).clean(*args,**kwargs)