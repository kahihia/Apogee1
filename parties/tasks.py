# tasks manages all of the celery processes we want 
# to happen with parties
from __future__ import absolute_import
from celery import shared_task

from .models import Party

# the shared task just makes it so the celery app can access this
@shared_task
# this method takes the list of joined, reorders it randomly, and picks one
def pick_winner(party_id):
	try:
		# gets the correct party
		# filter would return a queryset, we want an object.
		party = Party.objects.get(pk=party_id)
	except Party.DoesNotExist:
		# if the party is deleted, it does nothing
		return 

	# if there are people that joined the event
	if party.joined.all().count() > 0:
		#if the party event is a lottery
		# gets all users in joined, orders them randomly
		pool = party.joined.all().order_by('?')

		if party.event_type==1 and party.is_open:
			for i in range(0,party.num_possible_winners):
				if pool:
					winner = pool.first()
					print("Scheduler")
					print(i)
					print(winner)
					Party.objects.win_toggle(winner, party)
					winner = pool.exclude(pk=winner.pk)
			# print (pool)
			# # the winner is just the top of the random stack
			# winner = pool.first()
			# print (winner)
			# # use an add method to add the winner to winners many to many
			# #
			# print ('it worked')
		#If the party event is a bid
		elif party.event_type==2 and party.is_open:
			#Anyone in the joined list at the end of the event is a winner
			winners = party.joined.all()
			for w in winners:
				print (w)
			#add winners in
			for i in winners:
				Party.objects.win_toggle(i, party)
		elif party.event_type==3 and party.is_open:
			print("Buyout event is over")	

		party.is_open = False
		party.save2(update_fields=['is_open'])
		return party.id
	else:
		print ('it didnt work')
		party.is_open = False
		party.save2(update_fields=['is_open'])	
		return party.id



