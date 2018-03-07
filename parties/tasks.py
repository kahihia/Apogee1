from __future__ import absolute_import
from celery import shared_task

from .models import Party

@shared_task
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
		# gets all users in joined, orders them randomly
		pool = party.joined.all().order_by('?')
		print (pool)
		# the winner is just the top of the random stack
		winner = pool[0]
		print (winner)
		# use an add method to add the winner to winners many to many
		Party.objects.win_toggle(winner, party)
		print ('it worked')
		return party.id
	else:
		print ('it didnt work')
		return 