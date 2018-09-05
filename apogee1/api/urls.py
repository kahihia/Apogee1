# these are all the API views for events. they arent actually visible 
# without typing the url in directly
from django.urls import path
from django.views.generic import RedirectView

# views
from .views import (
		SetTimzoneEndpoint
	)

app_name = 'timezone-api'
# /api/events/ routes to this 
urlpatterns = [
    path('', SetTimzoneEndpoint.as_view(), name='list'),
    path('/email_test/', SetTimzoneEndpoint.as_view(), name='list'),
 ]