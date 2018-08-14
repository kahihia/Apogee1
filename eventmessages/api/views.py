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

logger = logging.getLogger(__name__)

# star toggle is a method from the model that just adds the user to the 
class EventMessageView(APIView):
	authentication_classes = [SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	def post(self, request, format=None):
		# gets the object that is being starred

		message_qs = Message.objects.filter(room__id=request.data['room_id']).order_by('timestamp')[:10].values()
		return Response({'messages': message_qs})
