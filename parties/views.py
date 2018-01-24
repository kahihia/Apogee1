from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
		ListView, 
		DetailView, 
		CreateView, 
		UpdateView, 
		DeleteView
	)

from .forms import PartyModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Party
# Create your views here.

class PartyDeleteView(UserOwnerMixin, LoginRequiredMixin, DeleteView):
	model = Party
	template_name = 'parties/delete_confirm.html'
	success_url = reverse_lazy('parties:list')


class PartyUpdateView(UserOwnerMixin, LoginRequiredMixin, UpdateView):
	queryset = Party.objects.all()
	form_class = PartyModelForm
	template_name = 'parties/update_view.html'


class PartyCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	# as of right now, the form does not have an easy way to input 
	# the date, it just has to be formatted properly.

	# for using a hybrid create/form view
	form_class = PartyModelForm
	template_name = 'parties/create_view.html'
	# success_url = reverse_lazy('parties:detail') doesnt work bc it needs pk

	# for if were doing straight createview
	# model = Party
	# fields = [
	# 		# 'user',
	# 		'title',
	# 		'description',
	# 		'party_time'
	# 	]


class PartyDetailView(LoginRequiredMixin, DetailView):
	queryset = Party.objects.all()
	# use 'template_name' to use a custom template name
	# pk == id by default. theyre the same term


class PartyListView(LoginRequiredMixin, ListView):
	def get_queryset(self, *args, **kwargs):
		qs = Party.objects.all()
		# this return the string form of the search passed into the url
		query = self.request.GET.get('q', None)
		if query is not None:
			# Q is a lookup function
			qs = qs.filter(
				Q(description__icontains=query) | 
				Q(user__username__icontains=query) | 
				Q(title__icontains=query)
				)
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(PartyListView, self).get_context_data(*args, **kwargs)
		return context


# these are the inner workings of how the class based views actually render
# def party_detail_view(request, id=1):
# 	obj = Party.objects.get(id=id) # gets from database
# 	print(obj)
# 	context = {
# 		'object': obj
# 	}
# 	return render(request, 'parties/detail_view.html', context)