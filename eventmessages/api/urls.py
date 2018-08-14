# these are all the API views for events. they arent actually visible 
# without typing the url in directly
from django.urls import path
from django.views.generic import RedirectView

# views
from .views import (
		EventMessageView
	)

app_name = 'parties-api'
# /api/messages/ routes to this 
urlpatterns = [
    path('', EventMessageView.as_view(), name='api-messages'),
   # url(r"^<int:pk>/join/(?P<dollar>\d+\.\d+)$", BidAPIView.as_view(), name="bid-toggle"), 
 ]