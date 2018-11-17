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


def add_money(user, amount):
	curr_balance = user.profile.account_balance + amount
	user.profile.account_balance = curr_balance
	user.profile.save(update_fields=['account_balance'])
#on outbid, returns bid_obj value to user account balance
#this function is never called currently because we have
#an on_delete method on bid object
#that serves the same purpose
def outbid_return(bid_obj):
	user = bid_obj.user
	curr_balance = user.profile.account_balance + bid_obj.bid_amount
	user.profile.account_balance = curr_balance
	user.profile.save(update_fields=['account_balance'])
#Gets all users associated with a party_obj
#Returns the event proceeds to user account_balance
#THIS FUNCTION IS NEVER CALLED BUT IS USED IN THE PARTY MODEL
def return_event_proceeds(party_obj):
	if party_obj.event_type==1:
		user_list = party_obj.joined
		for user in user_list:
			curr_balance = user.profile.account_balance - party_obj.cost
			user.profile.account_balance = curr_balance
			user.profile.save(update_fields=['account_balance'])
	elif party_obj.event_type==2:
		bid_list = Bid.objects.filter(party=party_obj)
		for bid in bid_list:
			user = bid.user
			curr_balance = user.profile.account_balance + bid.bid_amount
			user.profile.account_balance = curr_balance
			user.profile.save(update_fields=['account_balance'])
	else:
		user_list = party_obj.winners
		for user in user_list:
			curr_balance = user.profile.account_balance - party_obj.cost
			user.profile.account_balance = curr_balance
			user.profile.save(update_fields=['account_balance'])

#Create a payment object for party owner
def create_payment(party_obj):
	payment_amount = 0
	if party_obj.event_type==1:
		payment_amount = party_obj.joined.all().count() * party_obj.cost
	elif party_obj.event_type==2:
		bid_list = Bid.objects.filter(party=party_obj)
		for bids in bid_list:
			payment_amount+=bids.bid_amount
	else:
		payment_amount = party_obj.winners.all().count() * party_obj.cost

	EventPayment.objects.create(payment_user=party_obj.user, party=party_obj, \
		payment_amount=payment_amount)