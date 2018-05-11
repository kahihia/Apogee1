from django.shortcuts import render
from .models import Bid
from django.views.generic import ListView, DetailView
# Create your views here.

#Create View







#Retrieve Views (BidDetailView and BidListView)
class BidDetailView(DetailView):
	queryset = Bid.objects.all()
	def get_object(self):
		return Bid.objects.get(id=1)

#returns a query of all the Bids to list_view.html which prints out all of the bids
class BidListView(ListView):
	template_name = "bids/list_view.html"
	queryset = Bid.objects.all()
	def get_context_data(self, *args, **kwargs):
		context = super(BidListView, self).get_context_data(*args, **kwargs)
		print(context)
		return context

#deprecated function -- was replaced by BidDetailView
'''
def bid_list_view(request):
	
	qs = Bid.objects.all()
	context = {
		"object_list": qs
	}
	print(qs)
	
	return render(request,"bids/list_view.html", context)
'''