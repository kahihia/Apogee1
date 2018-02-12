from django.urls import path, include
from django.views.generic import RedirectView

# views
from .views import (
		UserDetailView, 
		UserFollowView, 
		UserProfileUpdateView
	)

app_name = 'profiles'
# /profiles routes to this 
urlpatterns = [
    path('<username>/', UserDetailView.as_view(), name='detail'), 
    path('<username>/follow/', UserFollowView.as_view(), name='follow'),
    path('<username>/edit/', UserProfileUpdateView.as_view(), name='edit'), 
]