def get_blocking_lists(request):
	"""
		Get the blocking and blocked by list from the user session
		* request - client request
		Return - Tuple
		(blocked_by_list, blocking_list)
		* blocked_by_list - all users that have blocked this user
		* blocking_list - all users this user is blocking
	"""
	if not request.user.is_authenticated:
		blocked_by_list = []
		blocking_list = []
	else:
		blocked_by_list = request.user.blocked_by.all() 
		blocking_list = request.user.profile.blocking.all()
	return (blocked_by_list, blocking_list)