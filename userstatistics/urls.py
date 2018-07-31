from django.urls import path

# views
from .views import (
		StatsListView
	)
app_name='statistics'

urlpatterns = [
	path('', StatsListView.as_view(), name = 'list'), # Goes to stats page /stats/
]