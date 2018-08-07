from django.conf.urls import include, url
from . import views

# app name specifies how we refer to these urls
# for example, the notificaitons page is "notifications:list"
app_name = 'eventmessages'

urlpatterns = [
    url(r'^$',  views.index, name='chat'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]