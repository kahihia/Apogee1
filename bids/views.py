# from django.forms.utils import ErrorList
# from django.shortcuts import render
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django import forms
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy


# from .mixins import FormUserNeededMixin, UserOwnerMixin
# from .models import Bid
# from .forms import BidModelForm, BidModelForm2
# # Create your views here.

# #Create View
# #Reached via /bids/create
# class BidCreateView(FormUserNeededMixin, CreateView):
# 	form_class = BidModelForm2
# 	template_name = 'bids/create_view.html'
# 	success_url = '/bids'
# 	def post(self, request, **kwargs):
# 		print(request.POST)
# 		return super(BidCreateView, self).post(request, **kwargs)
# 	def get_context_data(self, *args, **kwargs):
# 		queryset = Bid.objects.all()
# 		context = super(BidCreateView, self).get_context_data(*args, **kwargs)
# 		context['create_form'] = BidModelForm2
# 		context['create_url'] = reverse_lazy("bids:create")
# 		context['object_list'] = queryset

# 		return context

	
# #Look at update view tutorial for mixin on user updates and types of users allowed 
# #Update View
# #Reached via /bids/<int>/update
# class BidUpdateView(UserOwnerMixin, UpdateView):
# 	queryset = Bid.objects.all()
# 	form_class = BidModelForm2
# 	template_name = 'bids/update_view.html'
# 	success_url = '/bids/'


# #Retrieve Views (BidDetailView and BidListView)
# class BidDetailView(DetailView):
# 	queryset = Bid.objects.all()
# 	def get_object(self):
# 		return Bid.objects.get(id=1)

# #returns a query of all the Bids to list_view.html which prints out all of the bids
# class BidListView(ListView):
# 	template_name = "bids/list_view.html"
# 	queryset = Bid.objects.all()
# 	def get_context_data(self, *args, **kwargs):
# 		context = super(BidListView, self).get_context_data(*args, **kwargs)
# 		context['create_form'] = BidModelForm2
# 		context['create_url'] = reverse_lazy("bids:create")
# 		return context
# #Delete view
# class BidDeleteView(DeleteView):
# 	model = Bid
# 	template_name = 'bids/delete_confirm.html'
# 	success_url = reverse_lazy("bids:list")