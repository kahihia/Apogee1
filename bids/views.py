from django.shortcuts import render
from .models import Bid
# Create your views here.

def bid_list_view(request):
	
	qs = Bid.objects.all()
	context = {
		"object_list": qs
	}
	print(qs)
	
	return render(request,"bids/list_view.html", context)