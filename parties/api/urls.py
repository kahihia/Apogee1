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
	)

app_name = 'parties-api'
# /api/events/ routes to this 
urlpatterns = [
    path('', PartyListAPIView.as_view(), name='list'),
    path('starred/', StarredListAPIView.as_view(), name='starred-api'),
    path('create/', PartyCreateAPIView.as_view(), name='create'), 
    path('<int:pk>/', PartyDetailAPIView.as_view(), name='detail'),
    path('<int:pk>/star/', StarToggleAPIView.as_view(), name='star-toggle'), 
 ]