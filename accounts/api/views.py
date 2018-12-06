from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import UserProfile

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
			account = UserProfile.objects.get(email_auth_token=auth_key)
		except:
			return Response({'account_found':False})

		# account = account.first()
		if account:
			password_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
				user_obj.profile.password_reset_token = password_token
				user_obj.profile.save(update_fields=['password_reset_token'])
			# m = Mailin("https://api.sendinblue.com/v2.0", config('SENDINBLUE_V2_KEY'))
			# data = { "to" : {user_email:"to whom!"},
			# 	"from" : ["developers@apogee.gg", "Welcome to Granite!"],
			# 	"subject" : "Account Authentication",
			# 	"html" : "<h1>Welcome to Granite!</h1>\nYour account has been successfully registered!\n\
			# 	 Please visit https://www.granite.gg/authentication and enter in <strong>"+auth_token+"</strong> to authenticate your account"
			# 	}
			# result = m.send_email(data)
			return Response({'account_found':True})
		return Response({'account_found':False})
