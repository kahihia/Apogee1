# views tell us the templates and methods available to each page
# because this is the api, the views specify the action that happend upon visit
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

import logging
from ..models import Message
from decouple import config
from .pagination import StandardResultsPagination
from .serializers import MessageModelSerializer

logger = logging.getLogger(__name__)

# star toggle is a method from the model that just adds the user to the 
class EventMessageView(generics.ListAPIView):
	authentication_classes = [SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	pagination_class = StandardResultsPagination
	serializer_class = MessageModelSerializer
	def get_queryset(self, *args, **kwargs):
		# gets the object that is being starred
		message_qs = Message.objects.filter(room__id=self.kwargs.get('room_id'))
		return message_qs
