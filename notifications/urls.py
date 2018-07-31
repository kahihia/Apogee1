from django.urls import path

# views
from .views import NotificationListView

# app name specifies how we refer to these urls
# for example, the notificaitons page is "notifications:list"
app_name = 'notifications'
# /notifications routes to this 
urlpatterns = [
	path('', NotificationListView.as_view(), name='list'), # /notifications
]