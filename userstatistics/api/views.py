from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Count

from.serializers import StatisticsInfoModelSerializer
from userstatistics.models import StatisticsInfo


class StatsAPIListView(generics.ListAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = StatisticsInfoModelSerializer
	def get_queryset(self, format=None):
		qs = StatisticsInfo.objects.filter(user=self.request.user)
		return qs