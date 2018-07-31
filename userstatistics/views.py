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
		return qs