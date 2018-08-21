from bids.models import Bid
def return_funds(party_obj):
	if party_obj.event_type==1:
		user_list = party_obj.joined.all()
		for user in user_list:
			curr_balance = user.profile.account_balance + party_obj.cost
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
		user_list = party_obj.winners.all()
		for user in user_list:
			curr_balance = user.profile.account_balance + party_obj.cost
			user.profile.account_balance = curr_balance
			user.profile.save(update_fields=['account_balance'])