from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
		ListView
	)

from .models import StatisticsInfo

# Create your views here.
class StatsListView(LoginRequiredMixin, ListView):
	template_name = 'userstatistics/statistics_info_list.html'
	def get_queryset(self, *args, **kwargs):
		qs = StatisticsInfo.objects.get(user=self.request.user)

		# currently unused because the search goes to a different view
		# this return the string form of the search passed into the url
		# query = self.request.GET.get('q', None)
		# if query is not None:
		# 	# Q is a lookup function
		# 	qs = qs.filter(
		# 		Q(description__icontains=query) | 
		# 		Q(user__username__icontains=query) | 
		# 		Q(title__icontains=query)
		# 		)
		return qs