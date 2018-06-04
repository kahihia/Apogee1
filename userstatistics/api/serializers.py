from django.utils.timesince import timeuntil
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import timedelta

from userstatistics.models import StatisticsInfo 
from accounts.api.serializers import UserDisplaySerializer


class StatisticsInfoModelSerializer(serializers.ModelSerializer):
	user = UserDisplaySerializer(read_only=True) 
	total_earnings = serializers.SerializerMethodField()
	total_num_events = serializers.SerializerMethodField()
	general_average_earnings = serializers.SerializerMethodField()
	lottery_average_earnings = serializers.SerializerMethodField()
	bid_average_earnings = serializers.SerializerMethodField()
	buyout_average_earnings = serializers.SerializerMethodField()
	general_join_time = serializers.SerializerMethodField()
	general_join_event_time = serializers.SerializerMethodField()
	general_star_time = serializers.SerializerMethodField()
	general_star_event_time = serializers.SerializerMethodField()
	class Meta:
		# the API is built on the party model
		model = StatisticsInfo
		# the fields tell us what is in the API. some are Serilaizermethodfields 
		# the others are directly from the model
		fields = [
			'user',  #serialized
			'max_profit',
			'max_profit_event',
			'total_earnings', #serialized
			'total_num_events', #serialized 
			'general_average_earnings', #serialized
			'general_join_time',#serialized
			'general_join_event_time',#serialized
			'general_star_time', #serialized
			'general_star_event_time', #serialized
			'lottery_num_events',
			'lottery_total_earnings',
			'lottery_total_participants',
			'lottery_average_earnings', #serialized
			'lottery_join_time',
			'lottery_join_event_time',
			'lottery_star_time',
			'lottery_star_event_time',
			'bid_num_events',
			'bid_total_earnings',
			'bid_join_time',
			'bid_join_event_time',
			'bid_star_time',
			'bid_star_event_time',
			'bid_average_earnings', # serialized
			'max_bid_event',
			'buyout_num_events',
			'buyout_total_earnings',
			'buyout_join_time',
			'buyout_join_event_time',
			'buyout_star_time',
			'buyout_star_event_time',
			'buyout_average_earnings', # serialized



		]


	def get_general_join_event_time(self,obj):
		general_join_event=[0]*48
		buyout_join_event = obj.buyout_join_event_time 
		lottery_join_event = obj.lottery_join_event_time
		bid_join_event = obj.bid_join_event_time
		print("goodbye")
		for i in buyout_join_event:
			general_join_event[i]= buyout_join_event[i]+lottery_join_event[i]+\
			bid_join_event[i]
			print(general_join_event[i])
		print("hello")
		return general_join_event

	def get_general_join_time(self,obj):
		buyout_join = obj.buyout_join_time 
		lottery_join = obj.lottery_join_time
		bid_join = obj.bid_join_time
		for i in buyout_join:
			print(buyout_join[i])

	def get_general_star_time(self,obj):
		buyout_join = obj.buyout_join_time 
		lottery_join = obj.lottery_join_time
		bid_join = obj.bid_join_time
		for i in bid_join:
			print(bid_join[i])
	def get_general_star_event_time(self,obj):
		buyout_join = obj.buyout_join_time 
		lottery_join = obj.lottery_join_time
		bid_join = obj.bid_join_time
		for i in bid_join:
			print(bid_join[i])

	def get_buyout_average_earnings(self,obj):
		num_events = obj.buyout_num_events
		if num_events==0:
			return 0
		return obj.buyout_total_earnings/num_events

	def get_bid_average_earnings(self,obj):
		num_events = obj.bid_num_events
		if num_events==0:
			return 0
		return obj.bid_total_earnings/num_events

	def get_total_earnings(self, obj):
		return obj.bid_total_earnings+obj.buyout_total_earnings+\
		obj.lottery_total_earnings

	def get_total_num_events(self, obj):
		return obj.bid_num_events+obj.buyout_num_events+obj.lottery_num_events

	def get_general_average_earnings(self, obj):
		num_events = obj.bid_num_events+obj.buyout_num_events+\
		obj.lottery_num_events
		earnings = obj.bid_total_earnings+obj.buyout_total_earnings+\
		obj.lottery_total_earnings
		if num_events==0:
			return 0
		average_earnings = earnings/num_events
		return average_earnings

	def get_lottery_average_earnings(self,obj):
		if obj.lottery_num_events==0:
			return 0 
		return obj.lottery_total_earnings/obj.lottery_num_events