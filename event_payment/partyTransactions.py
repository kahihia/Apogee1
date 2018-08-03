from bids.models import Bid
from django.db.models.signals import post_save
import decimal
from .models import EventPayment
#Reduces the user's account balance by the bid amount
def bid_reduction(user, bid):
	curr_balance = user.profile.account_balance - decimal.Decimal(str(bid))
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
	user.profile.account_balance = curr_balance
	user.profile.save(update_fields=['account_balance'])
#Create a payment object for party owner
def create_payment(party_obj):
	payment_amount = 0
	if party_obj.event_type==1:
		payment_amount = party_obj.joined.all().count() * party_obj.cost
	elif party_obj.event_type==2:
		bid_list = Bid.objects.filter(pk=party_obj.pk)
		for bids in bid_list:
			payment_amount+=bids.bid_amount
	else:
		payment_amount = party_obj.winners.all().count() * party_obj.cost

	EventPayment.objects.create(user=party_obj.user, party=party_obj, \
		payment_amount=payment_amount)