from django.shortcuts import render
from django.views import View

# Create your views here.
from .models import HashTag

# this is the routing for our hashtag search page. you can only 
# get to it by clicking a hashtag in an event
class HashTagView(View):
	def get(self, request, hashtag, *args, **kwargs):
		obj, created = HashTag.objects.get_or_create(tag=hashtag)
		return render(request, 'hashtags/tag_view.html', {'obj': obj})