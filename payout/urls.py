from django.urls import path
from django.views.generic import RedirectView

# views
from .views import (
		PayoutCreateView,
		PayoutDetailView,
	)

# app name specifies how we refer to these urls
# for example, the event detail page is "parties:detail"
app_name = 'payout'
# /events routes to this 
urlpatterns = [
    path('info/', PayoutCreateView.as_view(), name='info'),
    path('success/', PayoutDetailView.as_view(), name='success'),
]