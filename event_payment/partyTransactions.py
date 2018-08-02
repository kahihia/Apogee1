from bids.models import Bid
from django.db.models.signals import post_save

#Reduces the user's account balance by the bid amount
def bid_reduction(user, bid):
	curr_balance -= bid
	#curr_balance = user.profile.account_balance - party_obj.cost
	user.profile.account_balance = curr_balance
	user.profile.save(update_fields=['account_balance'])
#Reduces the user's account balance by the cost of the party_obj
def buy_lottery_reduction(user, party_obj):
	curr_balance = user.profile.account_balance - party_obj.cost
	user.profile.account_balance = curr_balance
	user.profile.save(update_fields=['account_balance'])
#on outbid, returns bid_obj value to user account balance
def outbid_return(bid_obj):
	user = bid_obj.user
	curr_balance = user.profile.account_balance + bid_obj.bid_amount
	user.profile.save(update_fields=['account_balance'])
