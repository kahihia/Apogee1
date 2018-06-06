# these are all the API views for events. they arent actually visible 
# without typing the url in directly
from django.urls import path

# views
from .views import (
	NotificationListAPIView, 
	SeenAPIView, 
	CheckedNotificationsAPIView, 
	)

app_name = 'notifications-api'
# /api/notifications/ routes to this 
urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='list'),
    path('checked/', CheckedNotificationsAPIView.as_view(), name='checked'),
    path('<int:pk>/', SeenAPIView.as_view(), name='make-seen'),
 ]