# These views manage all the rendering and data for party based pages
# as a note, Delete, Create, Update, List, Detail are all built in views 
# for Django, so htye are a bit magicky
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


# userownermixin doesnt work here. it only works on the update view 
# because it is based on a form submission. It needs to be based purely
# on the requesting user. Right now that check is on the delete-confirm HTML
class PartyDeleteView(UserOwnerMixin, LoginRequiredMixin, DeleteView):
	model = Party
	template_name = 'parties/delete_confirm.html'
	success_url = reverse_lazy('parties:list')


# update takes the data from the already-created event and fill sthe form with it
# the mixins ensure only a logged in owner can access the page
class PartyUpdateView(UserOwnerMixin, LoginRequiredMixin, UpdateView):
	queryset = Party.objects.all()
	form_class = PartyModelForm
	template_name = 'parties/update_view.html'


# the two mixins both ensure that the user is logged so that no event can be created 
# without a user attached 
class PartyCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	# as of right now, the form does not have an easy way to input 
	# the date, it just has to be formatted properly.

	# for using a hybrid create/form view
	form_class = PartyModelForm
	template_name = 'parties/create_view.html'
	# success_url = reverse_lazy('parties:detail') doesnt work bc it needs a pk
	# It does reroute to the event detail page after creation, not sure why

	# for if were doing straight createview
	# model = Party
	# fields = [
	# 		# 'user',
	# 		'title',
	# 		'description',
	# 		'party_time'
	# 	]

# the mixin requires you to be logged in to view events
# because of the way the detail HTML is named, we don't need to 
# specify it here. model_view (party_detail this time) is recognized automatically
class PartyDetailView(LoginRequiredMixin, DetailView):
	queryset = Party.objects.all()
	# use 'template_name' to use a custom template name
	# pk == id by default. theyre the same term


# this is the main home page view. all the rendering is handled by the api and 
# JS in base. I believe the queryset isn't even used, its just required by Django
class PartyListView(LoginRequiredMixin, ListView):
	def get_queryset(self, *args, **kwargs):
		qs = Party.objects.all()
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

	# I believe that context is needed so that we can access the request user in the HTML
	def get_context_data(self, *args, **kwargs):
		context = super(PartyListView, self).get_context_data(*args, **kwargs)
		return context

# following list requires the same info as the party list, plus a template name
class FollowingListView(LoginRequiredMixin, ListView):
	template_name = 'parties/following_list.html'
	def get_queryset(self, *args, **kwargs):
		qs = Party.objects.all()
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(FollowingListView, self).get_context_data(*args, **kwargs)
		return context

# almost identical to party list. the query is handled by the API
class StarredListView(LoginRequiredMixin, ListView):
	template_name = 'parties/starred_list.html'
	def get_queryset(self, *args, **kwargs):
		qs = Party.objects.all()
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(StarredListView, self).get_context_data(*args, **kwargs)
		return context

# almost identical to party list. the query is handled by the API
class JoinedListView(LoginRequiredMixin, ListView):
	template_name = 'parties/joined_list.html'
	def get_queryset(self, *args, **kwargs):
		qs = Party.objects.all()
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(JoinedListView, self).get_context_data(*args, **kwargs)
		return context

		
# these are the inner workings of how the class based views actually render
# def party_detail_view(request, id=1):
# 	obj = Party.objects.get(id=id) # gets from database
# 	print(obj)
# 	context = {
# 		'object': obj
# 	}
# 	return render(request, 'parties/detail_view.html', context)