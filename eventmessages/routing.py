from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/events/(?P<room_id>[^/]+)/', consumers.ChatConsumer),
]