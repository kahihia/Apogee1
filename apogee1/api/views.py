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
import json
import logging
import pytz

from decouple import config

logger = logging.getLogger(__name__)

class SetTimzoneEndpoint(APIView):
	def post(self, request, format=None):
		if request.session:
			user_timezone = request.POST.get('django_timezone', 'America/New_York')
			request.session['django_timezone'] = user_timezone
			timezone.activate(user_timezone)
			return Response(user_timezone, status=status.HTTP_200_OK)
		else:
			return Response({'status': 404}, status=status.HTTP_403_FORBIDDEN)
