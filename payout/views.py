from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import FormUserNeededMixin
from .forms import PayoutModelForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Payout

class PayoutCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	form_class = PayoutModelForm
	template_name = 'payout/create_view.html'
	success_url = '/payout/success'
	def form_valid(self, form):
		form.instance.payout_user = self.request.user
		form.instance.payout_amount = self.request.user.profile.account_balance
		self.request.user.profile.account_balance = self.request.user.profile.account_balance - form.instance.payout_amount
		self.request.user.profile.save(update_fields=['account_balance'])
		return super(PayoutCreateView, self).form_valid(form)

class PayoutDetailView(LoginRequiredMixin, DetailView):
	template_name = 'payout/detail_view.html'
	def get_queryset(self, *args, **kwargs):
		qs = Payout.objects.filter(payout_user=self.request.user)
		return qs