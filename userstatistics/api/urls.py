# these are all the API views for events. they arent actually visible 
# without typing the url in directly
from django.urls import path
from django.views.generic import RedirectView

# views
from .views import (
	StatsAPIListView
	)

app_name = 'statistics-api'
# /api/events/ routes to this 
urlpatterns = [
    path('', StatsAPIListView.as_view(), name='list')
 ]