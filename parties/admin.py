from django.contrib import admin

# Register your models here.
from .models import Party
from .forms import PartyModelForm


class PartyModelAdmin(admin.ModelAdmin):
	# form = PartyModelForm
	# the meta refers to anything not explicitly in the fields
	# if we used the meta and not the form, it would auto use the
	# attributes from the model. this is so admin can edit user
	class Meta:
		model = Party

# so that you can access the model on the admin site
admin.site.register(Party, PartyModelAdmin)