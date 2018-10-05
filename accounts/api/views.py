from rest_framework.views import APIView
from rest_framework.response import Response

class AuthorizationAPIView(APIView):
	def get(self, request, auth_key, format=None):
		# party_qeryset = Party.objects.filter(pk=pk)
		# party_event_type = party_qeryset.first().event_type
		#if party_event is bid
		account = User.profile.objects.filter(email_auth_token=auth_key)
		if account:
			print("FOUND")
			return Response(True)

		print("Not Found")
		return Response(False)
