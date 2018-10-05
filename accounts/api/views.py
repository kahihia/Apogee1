from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import UserProfile

class AuthorizationAPIView(APIView):
	def get(self, request, auth_key, format=None):
		# party_qeryset = Party.objects.filter(pk=pk)
		# party_event_type = party_qeryset.first().event_type
		#if party_event is bid
		account = UserProfile.objects.filter(email_auth_token=auth_key)
		if account and account.is_authenticated == True:
			account.is_authenticated = True
			account.email_auth_token = ""
			account.save(update_fields=['email_auth_token'])
			account.save(update_fields=['is_authenticated'])
			return Response(True)

		print("Not Found")
		return Response(False)
