import requests
from decouple import config
import json
from accounts.models import UserProfile



# This is the Streamlabs Connect function from the settings page. It runs the normal Streamlabs auth 
# cycle, makes sure the account isn't already attached somewhere, and attaches the details 
# to the request user.
def get_streamlabs_details(code, user_obj):
	try:
		# Streamlabs auth step one. send back their code with our credentials to get user credentials
		streamlabs_client_id = config('STREAMLABS_CLIENT_ID')
		streamlabs_client_secret = config('STREAMLABS_CLIENT_SECRET')
		streamlabs_redirect_uri = config('STREAMLABS_REDIRECT_URI')
		# headers = {
		# 	'content-type': 'application/json',
		# 	'Client-id': streamlabs_client_id
		# }
		data = {
			"grant_type":"authorization_code",
			'client_id': streamlabs_client_id,
			'client_secret': streamlabs_client_secret,
			"redirect_uri": streamlabs_redirect_uri, 
			"code": code
		}
		url = "https://streamlabs.com/api/v1.0/token"
		streamlabs_response = requests.requests("POST", url, params=data)
		print(streamlabs_response.text)
		streamlabs_dict=json.loads(streamlabs_response.text)
		streamlabs_access_token = streamlabs_dict['access_token']
		streamlabs_refresh_token = streamlabs_dict['refresh_token']

		# check that the account isn't already attached somewhere
		connected_qs = UserProfile.objects.filter(streamlabs_access_token=streamlabs_access_token).exclude(user=user_obj)
		if connected_qs.count() > 0:
			return 0

		user_obj.profile.streamlabs_access_token = streamlabs_access_token
		user_obj.profile.streamlabs_refresh_token = streamlabs_refresh_token
		user_obj.profile.save(update_fields=['streamlabs_access_token'])
		user_obj.profile.save(update_fields=['streamlabs_refresh_token'])
		return 1

	except Exception as e:
		#failure on authenticating code from streamlabs
		return -1


def refresh_streamlabs_credentials(user_obj):
	try:
		twitch_client_id = config('TWITCH_CLIENT_ID')
		twitch_secret = config('TWITCH_SECRET')
		twitch_redirect_uri = config('TWITCH_REDIRECT_URI')
		params = (('grant_type', 'refresh_token'), ('refresh_token', user_obj.profile.twitch_refresh_token), ('Client-id', twitch_client_id), ('client_secret', twitch_secret),)

		response = requests.post('https://id.twitch.tv/oauth2/token?client_id='+twitch_client_id, params=params)
		twitch_dict=json.loads(response.text)
		print(twitch_dict)
		user_obj.profile.twitch_refresh_token = twitch_dict['refresh_token']
		user_obj.profile.twitch_OAuth_token = twitch_dict['access_token']
		user_obj.profile.save(update_fields=['twitch_refresh_token'])
		user_obj.profile.save(update_fields=['twitch_OAuth_token'])
		return True
	except Exception as e:
		print("refresh")
		print(e)
		return False