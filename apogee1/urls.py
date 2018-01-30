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
from django.conf import settings
from django.conf.urls.static import static

# views
from .views import home, SearchView, set_timezone
from parties.views import PartyListView
from hashtags.views import HashTagView
from hashtags.api.views import TagPartyAPIView
from parties.api.views import SearchPartyAPIView
from accounts.views import UserRegisterView


# django will try and match these starting from the top, 
# so make sure that this ordering will not screw up the routing
urlpatterns = [
    path('admin/', admin.site.urls),
    # this should migrate into the settings page at some point soon
    path('tz/', set_timezone, name='set_timezone'),
    path('', PartyListView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('search/', SearchView.as_view(), name='search'),
    path('api/search/', SearchPartyAPIView.as_view(), name='search-api'),
    path('events/', include('parties.urls', namespace='parties')), #instance namespace. the app_name attr is the application namespace
    path('api/events/', include('parties.api.urls', namespace='parties-api')),
    path('api/', include('accounts.api.urls', namespace='profiles-api')),
    path('profiles/', include('accounts.urls', namespace='profiles')),
    path('tags/<slug:hashtag>/', HashTagView.as_view(), name='hashtag'),
    path('api/tags/<slug:hashtag>/', TagPartyAPIView.as_view(), name='hashtag-api'),
]

if settings.DEBUG:
	urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

if settings.DEBUG:
    urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]





