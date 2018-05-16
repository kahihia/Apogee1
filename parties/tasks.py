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
		if party.event_type==1:
			# gets all users in joined, orders them randomly
			pool = party.joined.all().order_by('?')
			print (pool)
			# the winner is just the top of the random stack
			winner = pool.first()
			print (winner)
			# use an add method to add the winner to winners many to many
			Party.objects.win_toggle(winner, party)
			print ('it worked')
		#If the party event is a bid
		elif party.event_type==2:
			#Anyone in the joined list at the end of the event is a winner
			winners = party.joined.all()
			for w in winner:
				print (w)
			#add winners in
			for i in winners:
				Party.objects.win_toggle(i, party)		
		return party.id
	else:
		print ('it didnt work')
		return 