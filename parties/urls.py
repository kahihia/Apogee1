from django.urls import path
from django.views.generic import RedirectView

# views
from .views import (
		PartyDetailView, 
		PartyListView, 
		PartyCreateView,
		PartyUpdateView, 
		PartyDeleteView, 
		FollowingListView,
		StarredListView,
	)

app_name = 'parties'
# /events routes to this 
urlpatterns = [
	path('', RedirectView.as_view(url='/')), # redirects to home
    path('search/', PartyListView.as_view(), name='list'), # /search/?q=
    path('following/', FollowingListView.as_view(), name='following-list'), # /search/?q=
    path('starred/', StarredListView.as_view(), name='starred-list'),
    path('<int:pk>/', PartyDetailView.as_view(), name='detail'), # /1
    path('create/', PartyCreateView.as_view(), name='create'), # /create
    path('<int:pk>/update/', PartyUpdateView.as_view(), name='update'), # /1/update
    path('<int:pk>/delete/', PartyDeleteView.as_view(), name='delete'), # /1/delete
]