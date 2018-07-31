# urls determines the urls that link to which views. the views display the info
from django.urls import path, include
from django.views.generic import RedirectView

# views we link directly to
from .views import (
		UserDetailView, 
		UserFollowView, 
		UserBlockView,
		UserProfileUpdateView
	)

app_name = 'profiles'
# /profiles routes to this 
# names are how you lazy refer to pages
urlpatterns = [
    path('<username>/', UserDetailView.as_view(), name='detail'), 
    path('<username>/follow/', UserFollowView.as_view(), name='follow'),
    path('<username>/block/', UserBlockView.as_view(), name='block'),
    path('<username>/edit/', UserProfileUpdateView.as_view(), name='edit'), 
]