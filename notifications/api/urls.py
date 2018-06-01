# these are all the API views for events. they arent actually visible 
# without typing the url in directly
from django.urls import path

# views
from .views import NotificationListAPIView, SeenAPIView

app_name = 'notifications-api'
# /api/notifications/ routes to this 
urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='list'),
    path('<int:pk>/', SeenAPIView.as_view(), name='make-seen'),
 ]