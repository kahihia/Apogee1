from django.db import models
from django.conf import settings
# Create your models here.
class Notification(models.Model):
	action 				= models.CharField(max_length=10)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL,
						on_delete=models.CASCADE)
	timestamp 			= models.DateTimeField(auto_now=True)
	party 				= models.IntegerField(default = 0)
	seen 				= models.BooleanField(default=False)

	def __str__(self):
		return str(self.action)