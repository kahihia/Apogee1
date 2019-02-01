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
		ClosingSoonListAPIView,
		StarredListAPIView,
		BuyoutLotteryAPIView, 
		JoinedListAPIView,
		BidAPIView,
		PaypalVerificationAPI,
		ReportAPIView,
		RefreshAPIView, 
		PriorityQueueAPIView
	)

app_name = 'parties-api'
# /api/events/ routes to this 
urlpatterns = [
    path('', PartyListAPIView.as_view(), name='list'),
    path('verify/', PaypalVerificationAPI.as_view(), name='paypal-verify-api'),
    path('starred/', StarredListAPIView.as_view(), name='starred-api'),
    path('joined/', JoinedListAPIView.as_view(), name='joined-api'),
    path('create/', PartyCreateAPIView.as_view(), name='create'),
    path('trending/', TrendingListAPIView.as_view(), name='trending'),
    path('closing/', ClosingSoonListAPIView.as_view(), name='closing-soon'),
    path('<int:pk>/', PartyDetailAPIView.as_view(), name='detail'),
    path('<int:pk>/star/', StarToggleAPIView.as_view(), name='star-toggle'),
    path('<int:pk>/join/<bids>', BidAPIView.as_view(), name='bid-toggle'),
    path('<int:pk>/join/', BuyoutLotteryAPIView.as_view(), name='join-toggle'),
    path('<int:pk>/priorityjoin/', PriorityQueueAPIView.as_view(), name='priority-join-toggle'),
    path('<int:pk>/report/', ReportAPIView.as_view(), name='report'),
    path('<int:pk>/refresh/', RefreshAPIView.as_view(), name='refresh'),
   # url(r"^<int:pk>/join/(?P<dollar>\d+\.\d+)$", BidAPIView.as_view(), name="bid-toggle"), 
 ]