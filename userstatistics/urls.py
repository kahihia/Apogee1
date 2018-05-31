from django.urls import path
from django.views.generic import RedirectView

# views
from .views import (
		StatsListView
	)
app_name='statistics'

urlpatterns = [
	path('', StatsListView.as_view(), name = 'list'), # Goes to stats page /stats/
]