from django.urls import path
from django.views.generic import RedirectView

# This import allows us to use event list API, which we need to 
# display the events for the profile 
from accounts.api.views import (
		AuthorizationAPIView,
		PasswordResetAPIView,
		PasswordTokenAPIView,
		PasswordMatchAPIView, 
		BotAPIView, 
		TwitchBotAPIView
	)
from parties.api.views import (
		PartyListAPIView
	)

app_name = 'profiles-api'
# /api/ routes to this 
urlpatterns = [
	# this url is the event API for the particular profile
	path('glitchbot/', BotAPIView.as_view(), name='bot'),
	path('twitchbot/<channelID>/<userid>/<type>/', TwitchBotAPIView.as_view(), name='twitchbot'),
    path('<username>/events/', PartyListAPIView.as_view(), name='list'),
    path('<auth_key>/authorization/', AuthorizationAPIView.as_view(), name='authorization'),
    path('<email>/password_reset/', PasswordResetAPIView.as_view(), name='passwordreset'),
    path('<token>/token/', PasswordTokenAPIView.as_view(), name='passwordtoken'),
    path('<password>/password/<token>', PasswordMatchAPIView.as_view(), name='passwordmatch')
 ]