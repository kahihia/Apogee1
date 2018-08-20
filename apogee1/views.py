# Views tells us what each url does and how its rendered. 
# it also provides methods and the queryset for the page.
# there arent very many in this main app. 
import pytz
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q
from parties.models import Party
from parties.api.serializers import PartyModelSerializer
from django.utils import timezone
from datetime import timedelta


class TOSView(View):
	
# this is the default home page from when the app starts
class HomeView(View):
	def get(self, request, *args, **kwargs):
		# Maybe put this in middleware later
		blocked_by_list = self.request.user.blocked_by.all()
		blocking_list = self.request.user.profile.blocking.all()
		# Trending
		trending = Party.objects.filter(is_open=True).order_by('-popularity')[:6]
		serialized_trending = PartyModelSerializer(trending, many=True, context={'request': request}).data

		# Closing
		soon_time = timezone.now() + timedelta(minutes=15)
		closing = Party.objects.filter(is_open=True) \
							.filter(party_time__lte=soon_time) \
							.exclude(user__profile__in=blocked_by_list) \
							.exclude(user__in=blocking_list) \
							.order_by('-popularity')[:6]
		serialized_closing = PartyModelSerializer(closing, many=True, context={'request': request}).data
		# Following
		im_following = self.request.user.profile.get_following()
		if im_following:
			following = Party.objects.filter(user__in=im_following) \
								.filter(is_open=True) \
								.exclude(user__profile__in=blocked_by_list) \
								.exclude(user__in=blocking_list) \
								.order_by('-time_created')
			serialized_following = PartyModelSerializer(following, many=True, context={'request': request}).data
		else:
			serialized_following = None

		context = {'trending': serialized_trending, 'closing': serialized_closing, 'following': serialized_following, 'username': self.request.user.username}
		return render(request, 'home.html', context)

# we need this user model to search users 
User = get_user_model()

# this is the updated search view for the users and events
# events are done through ajax currently, django handles users
class SearchView(View):
	def get(self, request, *args, **kwargs):
		# grabbing url search terms
		# q refers to the key assigned into our search bar
		query = request.GET.get('q')
		qs = None
		if query:
			# this fills the query set passed to the search page with 
			# users that fit the search bar keyword
			qs = User.objects.filter(
					Q(username__icontains=query) 
				)
		context = {'users': qs, 'query': query}
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