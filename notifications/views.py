from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Notification

# Create your views here.
# this is the main home page view. all the rendering is handled by the api and 
# JS in base. I believe the queryset isn't even used, its just required by Django
class NotificationListView(LoginRequiredMixin, ListView):
	def get_queryset(self, *args, **kwargs):
		qs = Notification.objects.all()
		return qs