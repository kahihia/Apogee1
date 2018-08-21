"""apogee1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
# views
from .views import HomeView, SearchView, set_timezone, TOSView
from parties.views import PartyListView
from hashtags.views import HashTagView
from hashtags.api.views import TagPartyAPIView
from parties.api.views import SearchPartyAPIView
from accounts.views import UserRegisterView


# django will try and match these starting from the top, 
# so make sure that this ordering will not screw up the routing
# api tags is after api bacause it was mis-searching originally
# also, any line that has "include" refers to the urls.py files 
# in any of the other apps
# namespace is an instance namespace. the app_name attr is the application namespace
urlpatterns = [
	path('admin/', admin.site.urls),
	path('', PartyListView.as_view(), name='home'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('register/', UserRegisterView.as_view(), name='register'),
	path('search/', SearchView.as_view(), name='search'),
	path('api/search/', SearchPartyAPIView.as_view(), name='search-api'),
	path('api/payment/', include('parties.api.urls', namespace='parties-payment-api')),
	path('events/', include('parties.urls', namespace='parties')), 
	path('api/events/', include('parties.api.urls', namespace='parties-api')),
	path('api/messages/', include('eventmessages.api.urls', namespace='messages-api')),
	path('api/', include('accounts.api.urls', namespace='profiles-api')),
	path('api/statistics', include('userstatistics.api.urls', namespace='statistics-api')),
	path('profiles/', include('accounts.urls', namespace='profiles')),
	path('notifications/', include('notifications.urls', namespace='notifications')),
	path('api/notifications/', include('notifications.api.urls', namespace='notifications-api')),
	path('tags/<slug:hashtag>/', HashTagView.as_view(), name='hashtag'),
	path('api/tags/<slug:hashtag>/', TagPartyAPIView.as_view(), name='hashtag-api'),
	# this should migrate into the settings page at some point soon
	path('tz/', set_timezone, name='set_timezone'),
	path('stats/', include('userstatistics.urls', namespace='statistics')),
	path('payout/', include('payout.urls', namespace='payout')),
	path('tos', TOSView.as_view(), name='tos')
	#url(r'^.*$', RedirectView.as_view(url='', permanent=False), name='index')
	#Deprecated path to bids, bid views not available to users
	#path('bids/', include('bids.urls', namespace='bids'))
]

# adds our static files, like css, js
if settings.DEBUG:
	urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

# adds our media storage for things like thumbnails
if settings.DEBUG:
	urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

# im not sure why we do this twice. i think they do the exact same thing
if settings.DEBUG:
	urlpatterns += [
		re_path(r'^media/(?P<path>.*)$', serve, {
			'document_root': settings.MEDIA_ROOT,
		}),
	]





