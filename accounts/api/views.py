from rest_framework.views import APIView

class AuthorizationAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, auth_key, format=None):
		# party_qeryset = Party.objects.filter(pk=pk)
		# party_event_type = party_qeryset.first().event_type
		#if party_event is bid
		print(auth_key)	
		return Response()
