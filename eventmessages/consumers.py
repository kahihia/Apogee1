from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
import logging
from urllib import parse
from .models import Message, Room
from django.utils.html import escape

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        self.room_id = dict(parse.parse_qs(self.scope['query_string'].decode('utf-8')))['room_id'][0]
        logger.debug("Connect: room_id = " + self.room_id)
        self.room_group_name = 'chat_%s' % self.room_id
        self.room = Room.objects.get_or_create(pk=self.room_id)[0]
        self.room_name = "chat_%s" % self.room_id
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name,
        )
        await self.accept()


    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        await self.close()

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        if command == "send":
            m = escape(content["message"])
            Message.objects.create(message=m, room=self.room, username=self.scope['user'])
            await self.send_room(self.room_id, m)
        else:
            await self.send_json({'error': True})

    ##### Command helper methods called by receive_json

    async def send_room(self, room_id, message):
        """
        Called by receive_json when someone sends a message to a room.
        """
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat.message",
                "room_id": room_id,
                "username": self.scope["user"].username,
                "message": message,
            }
        )

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "room": event["room_id"],
                "username": escape(event["username"]),
                "message": escape(event["message"]),
            },
        )