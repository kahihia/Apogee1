import pytz
from django.shortcuts import render, redirect
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

# from django example for timezone 
# it currently renders to the tz_set html, but we'd like to migrate the form
# into a settings page, but if we just include the form html, we should be able to 
# keep this set to the same url. honestly not sure though
def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'tz_set.html', {'timezones': pytz.common_timezones})