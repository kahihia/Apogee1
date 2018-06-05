from .models import StatisticsInfo
from django.db.models import F
from parties import models
from bids import models
import datetime


##########################BUYOUT EVENT FUNCTIONS################################
def buyout_update_end_stats(party_obj):
	event_earnings = party_obj.winners.all().count() * party_obj.cost
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	if event_earnings > user_stats_page.max_profit:
		user_stats_page.max_profit = event_earnings
		user_stats_page.max_profit_event = party_obj.pk

	user_stats_page.buyout_num_events = F('buyout_num_events') + 1
	user_stats_page.buyout_total_earnings = F('buyout_total_earnings')\
											 + event_earnings
	user_stats_page.save(update_fields=['buyout_num_events',\
										'buyout_total_earnings',\
										'max_profit',
										'max_profit_event'
										])

def buyout_update_star_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_star_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	user_bucket = get_bucket(user_star_time)
	party_bucket = get_bucket(party_end_time)

	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.buyout_star_event_time
	temp_array[party_bucket] += 1
	user_stats_page.buyout_star_event_time = temp_array

	temp_array = user_stats_page.buyout_star_time
	temp_array[user_bucket] += 1
	user_stats_page.buyout_star_time = temp_array

	user_stats_page.save(update_fields=['buyout_star_time',\
										'buyout_star_event_time'\
										])


def buyout_update_join_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_join_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	user_bucket = get_bucket(user_join_time)
	party_bucket = get_bucket(party_end_time)

	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.buyout_join_event_time
	temp_array[party_bucket] += 1
	user_stats_page.buyout_join_event_time = temp_array

	temp_array = user_stats_page.buyout_join_time
	temp_array[user_bucket] += 1
	user_stats_page.buyout_join_time = temp_array

	user_stats_page.save(update_fields=['buyout_join_time',\
										'buyout_join_event_time'\
										])
######################LOTTO EVENT FUNCTIONS#####################################\
def lottery_update_end_stats(party_obj):
	print("Updating Stats for Ending of lottery")
	total_participants = party_obj.joined.all().count()
	event_earnings = total_participants * party_obj.cost
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	if event_earnings > user_stats_page.max_profit:
		user_stats_page.max_profit = event_earnings
		user_stats_page.max_profit_event = party_obj.pk

	user_stats_page.lottery_total_participants =\
							F('lottery_total_participants')+total_participants

	user_stats_page.lottery_num_events = F('lottery_num_events') + 1

	user_stats_page.lottery_total_earnings = F('lottery_total_earnings')\
											 + event_earnings

	user_stats_page.save(update_fields=['lottery_num_events',\
										'lottery_total_earnings',\
										'lottery_total_participants',\
										'max_profit',
										'max_profit_event'])

def lottery_update_star_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_star_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	user_bucket = get_bucket(user_star_time)
	party_bucket = get_bucket(party_end_time)

	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.lottery_star_event_time
	temp_array[party_bucket] += 1
	user_stats_page.lottery_star_event_time = temp_array

	temp_array = user_stats_page.lottery_star_time
	temp_array[user_bucket] += 1
	user_stats_page.lottery_star_time = temp_array

	user_stats_page.save(update_fields=['lottery_star_time',\
										'lottery_star_event_time'\
										])

def lottery_update_join_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_join_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	user_bucket = get_bucket(user_join_time)
	party_bucket = get_bucket(party_end_time)

	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.lottery_join_event_time
	temp_array[party_bucket] += 1
	user_stats_page.lottery_join_event_time = temp_array

	temp_array = user_stats_page.lottery_join_time
	temp_array[user_bucket] += 1
	user_stats_page.lottery_join_time = temp_array

	user_stats_page.save(update_fields=['lottery_join_time',\
										'lottery_join_event_time'\
										])


#####################BID EVENT FUNCTIONS########################################
def bid_update_end_stats(party_obj):
	bid_list = Bid.objects.filter(party=party_obj.pk)

	event_earnings = 0

	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)

	max_bid = user_stats_page.max_bid_event
	for bid in bid_list:
		event_earnings+=bid.bid_amount
		if bid.bid_amount > max_bid:
			max_bid = bid.bid_amount

	if event_earnings > user_stats_page.max_profit:
		user_stats_page.max_profit = event_earnings
		user_stats_page.max_profit_event = party_obj.pk
	user_stats_page.max_bid_event = max_bid
	user_stats_page.bid_num_events = F('bid_num_events') + 1
	user_stats_page.bid_total_earnings = F('bid_total_earnings')\
											 + event_earnings

	user_stats_page.save(update_fields=['bid_num_events',\
										'bid_total_earnings',\
										'max_bid_event',\
										'max_profit',
										'max_profit_event'
										])
def bid_update_star_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_star_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	user_bucket = get_bucket(user_star_time)
	party_bucket = get_bucket(party_end_time)

	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.bid_star_event_time
	temp_array[party_bucket] += 1
	user_stats_page.bid_star_event_time = temp_array

	temp_array = user_stats_page.bid_star_time
	temp_array[user_bucket] += 1
	user_stats_page.bid_star_time = temp_array

	user_stats_page.save(update_fields=['bid_star_time',\
										'bid_star_event_time'\
										])

def bid_update_join_stats(party_obj):
	user_stats_page = StatisticsInfo.objects.get(user=party_obj.user)
	user_join_time = datetime.datetime.now().time()
	party_end_time = party_obj.party_time.time()
	user_bucket = get_bucket(user_join_time)
	party_bucket = get_bucket(party_end_time)

	#Django doesn't like trying to modify individual cells in an array field
	#so, I copied the entire array over to a temp array, copied it back after
	#modifying it
	temp_array= user_stats_page.bid_join_event_time
	temp_array[party_bucket] += 1
	user_stats_page.bid_join_event_time = temp_array

	temp_array = user_stats_page.bid_join_time
	temp_array[user_bucket] += 1
	user_stats_page.bid_join_time = temp_array

	user_stats_page.save(update_fields=['bid_join_time',\
										'bid_join_event_time'\
										])
#############################GENERAL EVENT FUNCTIONS############################
def get_bucket(time):
	data_partitions_per_hour = 2
	minutes_in_hour = 60
	partition_bucket_number = data_partitions_per_hour*int(time.hour)
	if(int(time.minute)<minutes_in_hour/data_partitions_per_hour):
		return partition_bucket_number
	else:
		return partition_bucket_number+1

