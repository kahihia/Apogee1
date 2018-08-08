from django.contrib import admin

# Register your models here.
from .models import Payout
from .forms import PayoutModelForm

# not sure why this is written out differently from other admin files
class PayoutModelAdmin(admin.ModelAdmin):
	readonly_fields = ('payout_user', 'payout_amount', 'time_requested', 'description', 'payment_info',)
	# form = PayoutModelForm
	# the meta refers to anything not explicitly in the fields
	# if we used the meta and not the form, it would auto use the
	# attributes from the model. this is so admin can edit user
	class Meta:
		model = Payout

# so that you can access the model on the admin site
admin.site.register(Payout, PayoutModelAdmin)


payout_user 		= models.ForeignKey(
							settings.AUTH_USER_MODEL, 
							on_delete=models.CASCADE
						)
	payout_amount 		= models.DecimalField(max_digits=12, decimal_places=2, default=0)
	time_requested		= models.DateTimeField(auto_now_add=True)
	description 		= models.CharField(max_length=280)
	payment_info		= models.CharField(max_length=40)
	is_paid 			= models.BooleanField(default=False)