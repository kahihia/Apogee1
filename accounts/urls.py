# urls determines the urls that link to which views. the views display the info
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.views import PasswordResetView 

# views we link directly to
from .views import (
		FundsView, 
		UserDetailView, 
		UserFollowView, 
		UserBlockView,
		UserProfileUpdateView,
		UserDeleteView,
		UserTwitchAuthView
	)

app_name = 'profiles'
# /profiles routes to this 
# names are how you lazy refer to pages
urlpatterns = [
    path('<username>/', UserDetailView.as_view(), name='detail'), 
    path('<username>/follow/', UserFollowView.as_view(), name='follow'),
    path('<username>/block/', UserBlockView.as_view(), name='block'),
    path('<username>/edit/', UserProfileUpdateView.as_view(), name='edit'), 
    path('<username>/funds/', FundsView.as_view(), name='funds'), 	
    path('<username>/unregister/', UserDeleteView.as_view(), name='delete_user'),
    path('twitchauth/', UserTwitchAuthView.as_view()),  
]