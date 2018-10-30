import requests
from decouple import config
import json

def get_twitch_details(code, user_obj):
	try:
		twitch_client_id = config('TWITCH_CLIENT_ID')
		twitch_secret = config('TWITCH_SECRET')
		twitch_redirect_uri = config('TWITCH_REDIRECT_URI')
		headers = {
			'content-type': 'application/json',
			'Client-id': twitch_client_id
		}
		print("________________3_____________________________________")
		data = {
			"grant_type":"authorization_code",
			'client_id': twitch_client_id,
			"client_secret": twitch_secret,
			"code": code,
			"redirect_uri": twitch_redirect_uri
		}
		print(data)
		print("________________4_____________________________________")
		twitch_response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=json.dumps(data))
		print(twitch_response)
		twitch_dict=json.loads(twitch_response.text)
		# twitch_dict = twitch_functions.getOAuth(code)
		context={}
		print(twitch_dict)
		try:
			context['authenticated']=True
			twitch_oauth_token = twitch_dict['access_token']
			twitch_refresh_token = twitch_dict['refresh_token']
			auth_string = 'OAuth '
			auth_string+= twitch_oauth_token
			headers = {
				'Accept': 'application/vnd.twitchtv.v5+json',
				'Client-ID': twitch_client_id,
				'Authorization': auth_string,
			}
			response = requests.get('https://api.twitch.tv/kraken/channel', headers=headers)
			# response = twitch_functions.getChannelInfo(twitch_oauth_token)
			twitch_dict2 = json.loads(response.text)
			twitch_id = twitch_dict2['_id']
			print(twitch_dict2)
			user_obj = request.user
			user_obj.profile.twitch_id = twitch_id
			user_obj.profile.twitch_refresh_token = twitch_refresh_token
			user_obj.profile.twitch_OAuth_token = twitch_oauth_token
			user_obj.profile.save(update_fields=['twitch_id'])
			user_obj.profile.save(update_fields=['twitch_refresh_token'])
			user_obj.profile.save(update_fields=['twitch_OAuth_token'])
			return 1
		except:
			return 0
	except:
		#failure on authenticating code from twitch
		return -1


def getOAuth(code, user_obj):
	print(1)
	headers = {
	    'content-type': 'application/json',
	    'Client-id': 'f054futox6ybt8p07bndbqbuaw0v48'
	}
	data = {"grant_type":"authorization_code",'client_id': 'f054futox6ybt8p07bndbqbuaw0v48',
	"client_secret": "anu2ub103e0or8had2cn1h3d6yxtld","code":
	code,"redirect_uri": "https://granite.gg/profiles/twitchauth/confirmation/"}
	twitch_response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=json.dumps(data))
	twitch_dict=json.loads(twitch_response.text)
	print(twitch_dict)
	return twitch_dict

def getChannelInfo(OAuth):
	auth_string = 'OAuth '
	auth_string+= OAuth
	print(OAuth)
	headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': 'k6pbewo0iifuw2fu73rn9wz7k0beu1',
        'Authorization': auth_string,
	}

	response = requests.get('https://api.twitch.tv/kraken/channel', headers=headers)
	return response

def is_twitch_sub(party_owner, party_joiner):
	print("Checking that ")
	print(party_joiner.username)
	print(party_joiner.profile.twitch_id)
	print("is subscribed to")
	print(party_owner.username)
	print(party_owner.profile.twitch_id)

	try:
		print(0)
		if party_owner.twitch_id=="" or party_joiner.twitch_id=="":
			return False
		print(1)
		auth_string = 'OAuth '
		auth_string+= party_owner.twitch_OAuth_token
		headers = {'Accept': 'application/vnd.twitchtv.v5+json','Client-ID': 'k6pbewo0iifuw2fu73rn9wz7k0beu1','Authorization': auth_string,}
		new_url = 'https://api.twitch.tv/kraken/channels/'
		new_url+=party_owner.profile.twitch_id
		new_url+='/subscriptions/'
		new_url+=party_joiner.profile.twitch_id
		print(new_url)
		response = requests.get(new_url, headers=headers)
		twitch_dict=json.loads(response.text)
		print("TWITCH DICT IN TWITCH SUB")
		print(twitch_dict)
		has_sub = twitch_dict['sub_plan']
		if has_sub:
			print(2)
			return True
		else:
			print(3)
			return False
	except:
		refresh_twitch_credentials(party_owner)
		print("EXCEPTION IN TWITCH SUB")
		return False



def refresh_twitch_credentials(user_obj):
	try:
		params = (('grant_type', 'refresh_token'), ('refresh_token', user_obj.twitch_refresh_token), ('Client-id', 'k6pbewo0iifuw2fu73rn9wz7k0beu1'), ('client_secret', 'ycvbiwehveb5wodwaimdwdiho2rqs2'),)

		response = requests.post('https://id.twitch.tv/oauth2/token?client_id=k6pbewo0iifuw2fu73rn9wz7k0beu1', params=params)
		twitch_dict=json.loads(response.text)
		user_obj.profile.twitch_refresh_token = twitch_dict['refresh_token']
		user_obj.profile.twitch_OAuth_token = twitch_dict['access_token']
		user_obj.profile.save(update_fields=['twitch_refresh_token'])
		user_obj.profile.save(update_fields=['twitch_OAuth_token'])
		return True
	except:
		return False