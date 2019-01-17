from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import UserProfile
from django.contrib.auth.models import User
import json
import requests
import random
import string
from ast import literal_eval
from decouple import config
from mailin import Mailin

from apogee1.utils.twitch import twitch_functions


class BotAPIView(APIView):
	def get(self, request, format=None):
		return Response({'message':"YEET"})

class TwitchBotAPIView(APIView):
	def get(self, request, format=None):
		message = 'nope'
		try:
			data = (self.request.GET).dict()
			print(data)
			channel = data['channel']
			chatter = data['chatter']
			action = data['action']
			print(channel)
			print(chatter)
			print(action)
			if action == 'granite':
				# 'Granite' explains the basic commands and concept. 
				message = ('Granite allows you join events with your favorite creators. ' +
							'!graniteinfo will give you the event details, like type. !granitejoin will add you to the event. ' + 
							'!graniteplace will give you your place in line if the event is a queue')
			elif action == 'graniteinfo':
				# graniteinfo explains the event, so type, title, price
				message = twitch_functions.twitchBotInfo(channel)
			elif action == 'granitejoin':
				# join attempts to add the chatter to the event. it should return a message on failure only
				message = twitch_functions.twitchBotJoin(channel, chatter)
			elif action == 'granitenext':
				# next is a creator only, queue only command. it pulls the next x people in and says who they are. 
				# should also say who will get pulled in next
				# we want this to say who this is, so we'll need to attach names to our models. 
				if channel == chatter:
					message = twitch_functions.twitchBotNext(channel, chatter, 1)
				else:
					message = ''
			elif action == 'graniteplace':
				# this is a queue only command. returns the users place. 
				message = twitch_functions.twitchBotPlace(channel, chatter)
		except Exception as e:
			print(e)

		return Response({'message':message})

class AuthorizationAPIView(APIView):
	def get(self, request, auth_key, format=None):
		# party_qeryset = Party.objects.filter(pk=pk)
		# party_event_type = party_qeryset.first().event_type
		#if party_event is bid
		try:
			account = UserProfile.objects.get(email_auth_token=auth_key)
		except:
			return Response({'authenticated':False})

		# account = account.first()
		if account and account.is_authenticated==False:
			account.is_authenticated = True
			account.email_auth_token = ""
			account.save(update_fields=['email_auth_token'])
			account.save(update_fields=['is_authenticated'])
			return Response({'authenticated':True})
		return Response({'authenticated':False})

class PasswordResetAPIView(APIView):
	def get(self, request, email, format=None):
		try:
			account = User.objects.get(email=email)
			print("it worked")
		except:
			print("It didnt work")
			return Response({'account_found':False})

		# account = account.first()
		if account:
			password_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
			account.profile.password_reset_token = password_token
			account.profile.save(update_fields=['password_reset_token'])
			m = Mailin("https://api.sendinblue.com/v2.0", config('SENDINBLUE_V2_KEY'))
			data = { "to" : {email:"to whom!"},
				"from" : ["developers@apogee.gg", "Password Reset"],
				"subject" : "Password Reset",
				"html" : "<h1>Password Reset</h1>\n\
				Here is your password reset token: <strong>"+password_token+"</strong>"
				}
			result = m.send_email(data)
			return Response({'account_found':True})
		return Response({'account_found':False})

class PasswordTokenAPIView(APIView):
	def get(self, request, token, format=None):
		try:
			account = UserProfile.objects.get(password_reset_token=token)
			print("it worked")
		except:
			print("It didnt work")
			return Response({'token_found':False})

		# account = account.first()
		if account:
			return Response({'token_found':True})
		return Response({'token_found':False})

class PasswordMatchAPIView(APIView):
	def get(self, request, password, token, format=None):
		try:
			account = UserProfile.objects.get(password_reset_token=token)
		except:
			return Response({'password_reset':False})

		# account = account.first()
		if account:
			user = User.objects.get(profile=account)
			user.set_password(password)
			user.save()
			return Response({'password_reset':True})
		return Response({'password_reset':False})