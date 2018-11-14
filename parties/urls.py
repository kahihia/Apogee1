from django.urls import path
from django.views.generic import RedirectView

# views
from .views import (
		PartyDetailView, 
		PartyListView, 
		PartyCreateView,
		# PartyUpdateView, 
		PartyDeleteView, 
		FollowingListView,
		StarredListView,
		JoinedListView,
		PartyDuplicateView,
		PartyKickallView, 
	)

# app name specifies how we refer to these urls
# for example, the event detail page is "parties:detail"
app_name = 'parties'
# /events routes to this 
urlpatterns = [
# also note that <int:> just tells the url what type of input it can accept
	path('', RedirectView.as_view(url='/')), # redirects to home
    path('search/', PartyListView.as_view(), name='list'), # /search/?q=
    path('following/', FollowingListView.as_view(), name='following-list'), # /search/?q=
    path('starred/', StarredListView.as_view(), name='starred-list'),
    path('joined/', JoinedListView.as_view(), name='joined-list'),
    path('<int:pk>', PartyDetailView.as_view(), name='detail'), # /1
    path('create/', PartyCreateView.as_view(), name='create'), # /create
    # path('<int:pk>/update/', PartyUpdateView.as_view(), name='update'), # /1/update
    path('<int:pk>/delete/', PartyDeleteView.as_view(), name='delete'), # /1/delete
    path('<int:pk>/duplicate/', PartyDuplicateView.as_view(), name='duplicate'), # /1/duplicate
    path('<int:pk>/kickall/', PartyKickallView.as_view(), name='kickall'), # /1/duplicate
]