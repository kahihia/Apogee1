from django.db.models import F

lottery_mult = 1
bid_mult = 2
buyout_mult = 5

join_val = 10
star_val = 1

##############################Lottery Functions#################################
#adds popularity (scaled by event type)
def lottery_popularity_join(party_obj):
	party_obj.popularity = F('popularity') + (join_val*lottery_mult)
	party_obj.save2(update_fields=['popularity'])
# adds popularity
def lottery_popularity_star(party_obj):
	party_obj.popularity = F('popularity') + (star_val)
	party_obj.save2(update_fields=['popularity'])
# adds popularity
def lottery_popularity_unstar(party_obj):
	party_obj.popularity = F('popularity') - (star_val)
	party_obj.save2(update_fields=['popularity'])
##############################Bid Functions#####################################
#adds popularity (scaled by event type)
def bid_popularity_join(party_obj):
	party_obj.popularity = F('popularity') + (join_val*bid_mult)
	party_obj.save2(update_fields=['popularity'])
# adds popularity
def bid_popularity_star(party_obj):
	party_obj.popularity = F('popularity') + (star_val)
	party_obj.save2(update_fields=['popularity'])
# adds popularity
def bid_popularity_unstar(party_obj):
	party_obj.popularity = F('popularity') - (star_val)
	party_obj.save2(update_fields=['popularity'])
##############################buyout Functions#################################
#adds popularity (scaled by event type)
def buyout_popularity_join(party_obj):
	party_obj.popularity = F('popularity') + (join_val*buyout_mult)
	party_obj.save2(update_fields=['popularity'])
# adds popularity
def buyout_popularity_star(party_obj):
	party_obj.popularity = F('popularity') + (star_val)
	party_obj.save2(update_fields=['popularity'])
# adds popularity
def buyout_popularity_unstar(party_obj):
	party_obj.popularity = F('popularity') - (star_val)
	party_obj.save2(update_fields=['popularity'])