from django.urls import path
from django.views.generic import RedirectView

# This import allows us to use event list API, which we need to 
# display the events for the profile 
from accounts.api.views import (
		AuthorizationAPIView,
		PasswordResetAPIView
	)
from parties.api.views import (
		PartyListAPIView
	)

app_name = 'profiles-api'
# /api/ routes to this 
urlpatterns = [
	# this url is the event API for the particular profile
    path('<username>/events/', PartyListAPIView.as_view(), name='list'),
    path('<auth_key>/authorization/', AuthorizationAPIView.as_view(), name='authorization'),
    path('<email>/password_reset/', PasswordResetAPIView.as_view(), name='passwordreset')

 ]