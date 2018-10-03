# views tell us the templates and methods available to each page
# because this is the api, the views specify the action that happend upon visit
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from decimal import Decimal
from apogee1.utils.email import emailer
import json
import logging
import pytz

from decouple import config

logger = logging.getLogger(__name__)

class SetTimzoneEndpoint(APIView):
	def post(self, request, format=None):
		if request.session:
			user_timezone = request.data.get('django_timezone', 'America/New_York')
			request.session['django_timezone'] = user_timezone
			timezone.activate(user_timezone)
			return Response(user_timezone, status=status.HTTP_200_OK)
		else:
			return Response({'status': 404}, status=status.HTTP_403_FORBIDDEN)


class TestEmailEndpoint(APIView):
	"""
		Test endpoint to test if emails work as expected, post data to it as explained below
		* Disabled Via DISABLE_TEST_EMAILS env variable
		- POST PAYLOAD
		* email_to_send - a string referencing the template path you want to render
		* to_address - a string to send out
		* email_data - data sent to be rendered into the email
	"""
	def post(self, request, format=None):
		if config('DISABLE_TEST_EMAILS', default=True):
			return Response({'status' : '403 Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
		email_to_send = request.data.get('email_to_send')
		to_address = request.data.get('to_address')
		email_data = request.data.get('email_data', {'username': 'default username - could not get email_data from data'})
		if not email_to_send or not to_address or not email_data:
			return Response({'status' : '400 BAD REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

		# emailer.email('Test Email - Apogee Dev', 'devteam@mail.granite.gg', [to_address], email_to_send, email_data)
		# return Response({ 'status': '200 OK'}, status=status.HTTP_200_OK)

