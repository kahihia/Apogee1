# these are all the API views for events. they arent actually visible 
# without typing the url in directly
from django.urls import path
from django.views.generic import RedirectView

# views
from .views import (
		PartyListAPIView, 
		PartyCreateAPIView, 
		PartyDetailAPIView,  
		StarToggleAPIView, 
		TrendingListAPIView, 
		StarredListAPIView,
		BuyoutLotteryAPIView, 
		JoinedListAPIView,
		BidAPIView
	)

app_name = 'parties-api'
# /api/events/ routes to this 
urlpatterns = [
    path('', PartyListAPIView.as_view(), name='list'),
    path('starred/', StarredListAPIView.as_view(), name='starred-api'),
    path('joined/', JoinedListAPIView.as_view(), name='joined-api'),
    path('create/', PartyCreateAPIView.as_view(), name='create'), 
    path('<int:pk>/', PartyDetailAPIView.as_view(), name='detail'),
    path('<int:pk>/star/', StarToggleAPIView.as_view(), name='star-toggle'),
    path('<int:pk>/join/<int:bids>', BidAPIView.as_view(), name='bid-toggle'),
    path('<int:pk>/join/', BuyoutLotteryAPIView.as_view(), name='join-toggle') 
 ]