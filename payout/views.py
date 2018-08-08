from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import FormUserNeededMixin
from .forms import PayoutModelForm
# Create your views here.
from django.views.generic import CreateView

class PayoutCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	form_class = PayoutModelForm
	template_name = 'payout/create_view.html'