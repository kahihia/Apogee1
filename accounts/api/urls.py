from django.urls import path
from django.views.generic import RedirectView

# This import allows us to use event list API, which we need to 
# display the events for the profile 
from parties.api.views import (
		PartyListAPIView
	)

app_name = 'profiles-api'
# /api/ routes to this 
urlpatterns = [
	# this url is the event API for the particular profile
    path('<username>/events/', PartyListAPIView.as_view(), name='list'),
 ]