from django.contrib import admin

# Register your models here.
from .models import Bid
from .forms import BidModelForm


class BidModelAdmin(admin.ModelAdmin):
	form = BidModelForm
	# class Meta:
	# 	model = Bid


# this allows the admin site to access and edit the userprofile model
admin.site.register(Bid, BidModelAdmin)
