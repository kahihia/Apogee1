from django.conf.urls import include, url
from . import views

# app name specifies how we refer to these urls
# for example, the notificaitons page is "notifications:list"
app_name = 'eventmessages'

urlpatterns = [
    # url(r'^$',  views.about, name='about'),
    # url(r'^new/$', views.new_room, name='new_room'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]