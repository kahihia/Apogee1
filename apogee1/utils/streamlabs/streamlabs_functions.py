import requests
import urllib3
from decouple import config
import json
from django.utils.http import urlencode
from accounts.models import UserProfile


# This is the Streamlabs Connect function from the settings page. It runs the normal Streamlabs auth 
# cycle, makes sure the account isn't already attached somewhere, and attaches the details 
# to the request user.
def get_streamlabs_details(code, user_obj):
	try:
		print('were starting streamlabs details')
		print(code)
		# Streamlabs auth step one. send back their code with our credentials to get user credentials
		streamlabs_client_id = config('STREAMLABS_CLIENT_ID')
		streamlabs_client_secret = config('STREAMLABS_CLIENT_SECRET')
		streamlabs_redirect_uri = config('STREAMLABS_REDIRECT_URI')
		# headers = {
		# 	'content-type': 'application/json',
		# 	'Client-id': streamlabs_client_id
		# }
		querydict = {
			"grant_type":"authorization_code",
			"client_id":streamlabs_client_id,
			"client_secret":streamlabs_client_secret,
			"redirect_uri":streamlabs_redirect_uri, 
			"code":code
		}
		url = "https://streamlabs.com/api/v1.0/token"
		print('trying to post to streamlabs')

		# post request with requests
		# streamlabs_response = requests.request("POST", url, data=querydict)
		# streamlabs_response = requests.post("https://streamlabs.com/api/v1.0/token", data=json.dumps(querydict))
		
		# post request with urllib3
		http = urllib3.PoolManager()
		raw_response = http.request('POST',"https://streamlabs.com/api/v1.0/token", fields=querydict)
		streamlabs_dict = json.loads(raw_response.data.decode('utf-8'))

		print('got a response')
		# print(streamlabs_response.text)
		# streamlabs_dict=json.loads(streamlabs_response.text)
		streamlabs_access_token = streamlabs_dict['access_token']
		streamlabs_refresh_token = streamlabs_dict['refresh_token']
		print("token " + streamlabs_access_token)
		print("refresh " + streamlabs_refresh_token)

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
		print('got an exception')
		#failure on authenticating code from streamlabs
		return -1

# this is called when a streamlabs call fails. It sends the appropriate info back to 
# streamlabs to get a new access and refresh token
def refresh_streamlabs_credentials(user_obj):
	try:
		# Streamlabs auth step one. send back their code with our credentials to get user credentials
		streamlabs_client_id = config('STREAMLABS_CLIENT_ID')
		streamlabs_client_secret = config('STREAMLABS_CLIENT_SECRET')
		streamlabs_redirect_uri = config('STREAMLABS_REDIRECT_URI')

		querydict = {
			"grant_type":"refresh_token",
			'client_id': streamlabs_client_id,
			'client_secret': streamlabs_client_secret,
			"redirect_uri": streamlabs_redirect_uri, 
			"refresh_token": user_obj.profile.streamlabs_refresh_token
		}
		url = "https://streamlabs.com/api/v1.0/token"

		# using requests library
		# streamlabs_response = requests.requests("POST", url, params=data)
		# print(streamlabs_response.text)
		# streamlabs_dict=json.loads(streamlabs_response.text)

		# post request with urllib3
		http = urllib3.PoolManager()
		raw_response = http.request('POST',"https://streamlabs.com/api/v1.0/token", fields=querydict)
		streamlabs_dict = json.loads(raw_response.data.decode('utf-8'))

		print(streamlabs_dict)

		streamlabs_access_token = streamlabs_dict['access_token']
		streamlabs_refresh_token = streamlabs_dict['refresh_token']
		print("token " + streamlabs_access_token)
		print("refresh " + streamlabs_refresh_token)

		user_obj.profile.streamlabs_access_token = streamlabs_access_token
		user_obj.profile.streamlabs_refresh_token = streamlabs_refresh_token
		user_obj.profile.save(update_fields=['streamlabs_access_token'])
		user_obj.profile.save(update_fields=['streamlabs_refresh_token'])
		return True
	except Exception as e:
		return False

# this function actually creates an alert on the appropriate event when a fan joins
def send_streamlabs_alert(party_obj, user_obj):
	print('REEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!')
	try:
		access_token = party_obj.user.profile.streamlabs_access_token
		print('GOT ACCESS TOKEN')
		message = user_obj.username + ' has joined a Granite event for $' + str(party_obj.cost) + '!'


		# optional formatting
		# message = user_obj.username
		# user_message = 'Joined a Granite event for $' + party_obj.cost + '!'

		print('WERE IN THE ALERT FUNCTION')
		if access_token == '':
			print('THE ACCESS TOKEN WASNT THERE')
			return False

		querydict = {
			"access_token": access_token,
			'type': "donation",
			'message': message
		}
		url = "https://streamlabs.com/api/v1.0/alerts"

		print('POSTING ALERT 1')

		# api call using requests
		# streamlabs_response = requests.requests("POST", url, params=data)
		# print(streamlabs_response.text)
		# streamlabs_dict=json.loads(streamlabs_response.text)

		# post request with urllib3
		http = urllib3.PoolManager()
		raw_response = http.request('POST',"https://streamlabs.com/api/v1.0/alerts", fields=querydict)
		streamlabs_dict = json.loads(raw_response.data.decode('utf-8'))
		success = streamlabs_dict.get('success', False)

		print('POSTED ALERT? ' + success)

		# if it didnt work, we should try and refresh the token
		if success == False:
			print('refreshing')
			refresh_success = refresh_streamlabs_credentials(party_obj.user)
			print('did it refresh? ' + refresh_success)
			if refresh_success == True:
				access_token = party_obj.user.profile.streamlabs_access_token
				data = {
					"access_token": access_token,
					'type': "donation",
					'message': message
				}
				url = "https://streamlabs.com/api/v1.0/alerts"

				print('sending alert 2')
				# post request with urllib3
				http = urllib3.PoolManager()
				raw_response = http.request('POST',"https://streamlabs.com/api/v1.0/alerts", fields=querydict)
				streamlabs_dict = json.loads(raw_response.data.decode('utf-8'))
				success = streamlabs_dict.get('success', False)

				print('alert 2 sent? ' + success)
		
	except Exception as e:
		success = False
	return success