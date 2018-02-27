from celery import Celery

from .models import Party

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def pick_winner(party_id):
	try:
		# gets the correct party
		party = Party.objects.get(id=party_id)
	except Party.DoesNotExist:
		# if the party is deleted, it does nothing
		return 

	# gets all users in joined, orders them randomly
	pool = party.joined.all().order_by('?')
	# the winner is just the top of the random stack
	winner = pool[0]
	return winner

