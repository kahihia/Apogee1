from decouple import config

def configs(request):
	context_data = dict()
	context_data['hide_funding'] = config('HIDE_FUNDING', False)
	return context_data