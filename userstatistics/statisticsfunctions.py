from .models import StatisticsInfo
from django.db.models import F
from parties import models
import datetime


################################EVENT FUNCTIONS################################
def end_buyout_stats(party_obj):
	event_earnings = party_obj.winners.all().count() * party_obj.cost
	event_time = party_obj.party_time.time()
	user_stats_page = StatisticsInfo.objects.get(pk=party_obj.user.id)
	print(event_earnings)
	print(event_time)
	print("The event bucket is")

	print(user_stats_page.bid_join_time[1])
	user_stats_page.buyout_num_events = F('buyout_num_events') + 1
	user_stats_page.buyout_total_earnings = F('buyout_total_earnings')\
											 + event_earnings
	user_stats_page.save(update_fields=['buyout_num_events',\
										'buyout_total_earnings'\
										])

def buyout_starred_stats(party_obj):
	user_star_time = datetime.datetime.now().time()
	print(user_star_time)

def buyout_joined_stats(party_obj):
	user_join_time = datetime.datetime.now().time()
	print(user_join_time)
	
def get_bucket(time):
	data_partitions_per_hour = 2
	minutes_in_hour = 60
	partition_bucket_number = data_partitions_per_hour*int(time.hour)
	if(int(time.minute)<minutes_in_hour/data_partitions_per_hour):
		return partition_bucket_number
	else:
		return partition_bucket_number+1

