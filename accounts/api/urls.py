from django.urls import path
from django.views.generic import RedirectView

# views
from parties.api.views import (
		PartyListAPIView
	)

app_name = 'profiles-api'
# /api/ routes to this 
urlpatterns = [
    path('<username>/events/', PartyListAPIView.as_view(), name='list'),
 ]