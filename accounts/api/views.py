from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import UserProfile

class AuthorizationAPIView(APIView):
	def get(self, request, auth_key, format=None):
		# party_qeryset = Party.objects.filter(pk=pk)
		# party_event_type = party_qeryset.first().event_type
		#if party_event is bid
		print(1)
		try:
			print(2)
			account = UserProfile.objects.get(email_auth_token=auth_key)
			print(3)
		except:
			print(4)
			return Response({'authenticated':"true"})

		# account = account.first()
		print(5)
		if account and account.is_authenticated==False:
			print(6)
			account.is_authenticated = True
			print(7)
			account.email_auth_token = ""
			print(8)
			account.save(update_fields=['email_auth_token'])
			print(9)
			account.save(update_fields=['is_authenticated'])
			print(10)
			return Response({'authenticated':"true"})
		print(11)
		return Response({'authenticated':"true"})
