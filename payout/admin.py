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
