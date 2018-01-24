from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q

def home(request):
	return render(request, 'home.html', {})

User = get_user_model()
# this is the updated search view for the users and events
# events are doen through ajax currently, django handles users
class SearchView(View):
	def get(self, request, *args, **kwargs):
		# grabbing url search terms
		query = request.GET.get('q')
		qs = None
		if query:
			qs = User.objects.filter(
					Q(username__icontains=query) 
				)
		context = {'users': qs}
		return render(request, 'search.html', context)
