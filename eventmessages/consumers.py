from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import logging
from urllib import parse

logger = logging.getLogger(__name__)

def convert(data):
    if isinstance(data, bytes):  return data.decode('utf-8')
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = dict(parse.parse_qs(self.scope['query_string'].decode('utf-8')))['room_id'][0]
        logger.debug("Connect: room_id = " + self.room_id)
        self.room_group_name = 'chat_%s' % self.room_id
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.room_id
        )

        self.accept()

    def disconnect(self, close_code):
        logger.debug("Left room: " + self.room_id)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.room_id
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        Message.objects.create(message=message, room=room_group_name)
        logger.debug("Recieved: " + message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        logger.debug("Chat Recieved: " + message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))