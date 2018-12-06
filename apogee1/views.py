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
from apogee1.utils.auth.auth import get_blocking_lists
from django.shortcuts import redirect, render

User = get_user_model()


class PPView(View):
	def get(self, request, *args, **kwargs):
		context={'request':request}
		return render(request, 'privacypolicy.html', context)

class FeesView(View):
	def get(self, request, *args, **kwargs):
		context={'request':request}
		return render(request, 'fees.html', context)

class ConductView(View):
	def get(self, request, *args, **kwargs):
		context={'request':request}
		return render(request, 'conduct.html', context)

class ContactView(View):
	def get(self, request, *args, **kwargs):
		context={'request':request}
		return render(request, 'contact.html', context)

class AboutView(View):
	def get(self, request, *args, **kwargs):
		context={'request':request}
		return render(request, 'about.html', context)

class FAQView(View):
	def get(self, request, *args, **kwargs):
		context={'request':request}
		return render(request, 'FAQ.html', context)

class TOSView(View):
	def get(self, request, *args, **kwargs):
		context={'request':request}
		return render(request, 'tos.html', context)

class BlankView(View):
	def get(self, request, *args, **kwargs):
		context={'request':request}
		return render(request, 'blank.html', context)

class AuthenticationView(View):
	def get(self, request, *args, **kwargs):
		context={'request':request}
		return render(request, 'authentication.html', context)

class PasswordResetView(View):
	def get(self, request, *args, **kwargs):
		context={'request':request}
		return render(request, 'passwordreset.html', context)

# Error Pages
def server_error(request):
    return render(request, '500.html')
 
def not_found(request):
    return render(request, '404.html')
 
def permission_denied(request):
    return render(request, '403.html')
 
def bad_request(request):
    return render(request, '400.html')

# this is the default home page from when the app starts
class HomeView(View):
	def get(self, request, *args, **kwargs):
		# Maybe put this in middleware later
		trending = None
		closing = None
		following = None
		serialized_following = None
		blocked_by_list, blocking_list = get_blocking_lists(request)

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
		if request.user.is_authenticated:
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