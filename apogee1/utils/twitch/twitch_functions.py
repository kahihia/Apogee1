import requests
from decouple import config
import json
from django.contrib.auth import get_user_model, login
from accounts.models import UserProfile

from apogee1.utils.email import emailer
from parties.models import Party

User = get_user_model()



############################# TWITCH BOT FUNCITONS ############################

# graniteinfo explains the event, so type, title, price
def twitchBotInfo(channel):
	partyset = Party.objects.filter(user__profile__twitch_id=channel).filter(is_open=True).order_by('-time_created')
	if partyset.count() == 0:
		return 'No active events'
	event = partyset.first()
	name = event.user.username
	event_type = event.get_event_type_display()
	event_title = event.title
	event_price = event.cost
	msg = name + "'s event, \"" + event_title + '" is a ' + event_type + '.'
	if event_price != 0:
		msg += ' It costs $' + str(event_price) + ' to enter.' 
	return msg

def twitchBotJoin(channel, chatter):
	return 'join'

def twitchBotNext(channel, chatter, count):
	return 'next ' + str(count)

def twitchBotPlace(channel, chatter):
	return 'place'


######################### TWITCH CONNECTION FUNCTIONS #########################

# This is the Twitch Connect function from the settings page. It runs the normal Twitch auth 
# cycle, makes sure the account isn't already attached somewhere, and attaches the details 
# to the request user. this should be updated to check if the account is attached elsewhere. 
def get_twitch_details(code, user_obj):
	try:
		# twitch auth step one. send back their code with our credentials to get user credentials
		twitch_client_id = config('TWITCH_CLIENT_ID')
		twitch_secret = config('TWITCH_SECRET')
		twitch_redirect_uri = config('TWITCH_REDIRECT_URI')
		headers = {
			'content-type': 'application/json',
			'Client-id': twitch_client_id
		}
		data = {
			"grant_type":"authorization_code",
			'client_id': twitch_client_id,
			"client_secret": twitch_secret,
			"code": code,
			"redirect_uri": twitch_redirect_uri
		}
		twitch_response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=json.dumps(data))
		twitch_dict=json.loads(twitch_response.text)
		context={}
		try:
			# Twitch auth step 2. send user credentials to get user data back
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
			response = requests.get('https://api.twitch.tv/kraken/user', headers=headers)
			twitch_dict2 = json.loads(response.text)
			print(twitch_dict2)
			twitch_id = twitch_dict2['_id']

			# check that the account isn't already attached somewhere
			connected_qs = UserProfile.objects.filter(twitch_id=twitch_id).exclude(user=user_obj)
			if connected_qs.count() > 0:
				return 2

			# take the data and attach it to the profile
			user_obj.profile.twitch_id = twitch_id
			user_obj.profile.twitch_refresh_token = twitch_refresh_token
			user_obj.profile.twitch_OAuth_token = twitch_oauth_token
			user_obj.profile.save(update_fields=['twitch_id'])
			user_obj.profile.save(update_fields=['twitch_refresh_token'])
			user_obj.profile.save(update_fields=['twitch_OAuth_token'])
			return 1
		except Exception as e:
			return 0
	except:
		#failure on authenticating code from twitch
		return -1

# This is the Twitch Register function. It runs the normal Twitch auth cycle, 
# checks if the account is connected elsewhere, check that the email is available, 
# checks if the Twitch display name is available, and then creates the user and logs them in
def register_with_twitch(request, code):
	try:
		# twitch auth step one. send back their code with our credentials to get user credentials
		twitch_client_id = config('TWITCH_REGISTER_CLIENT_ID')
		twitch_secret = config('TWITCH_REGISTER_SECRET')
		twitch_redirect_uri = config('TWITCH_REGISTER_REDIRECT_URI')
		headers = {
			'content-type': 'application/json',
			'Client-id': twitch_client_id
		}
		data = {
			"grant_type":"authorization_code",
			'client_id': twitch_client_id,
			"client_secret": twitch_secret,
			"code": code,
			"redirect_uri": twitch_redirect_uri
		}
		twitch_response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=json.dumps(data))
		twitch_dict=json.loads(twitch_response.text)
		context={}
		try:
			# Twitch auth step 2. send user credentials to get user data back
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
			response = requests.get('https://api.twitch.tv/kraken/user', headers=headers)
			twitch_dict2 = json.loads(response.text)
			print(twitch_dict2)
			twitch_id = twitch_dict2['_id']
			twitch_name = twitch_dict2['display_name']
			twitch_email = twitch_dict2['email']

			# check availability of account, then name
			connected_qs = UserProfile.objects.filter(twitch_id=twitch_id)
			email_qs = User.objects.filter(email__iexact=twitch_email)
			username_qs = User.objects.filter(username__iexact=twitch_name)

			if connected_qs.count() > 0:
				# account already in use, please log in
				return 2
			if email_qs.count() > 0:
				# email already in use, please log in
				return 3
			if username_qs.count() > 0:
				# twitch username already in use, register manually
				return 4

			# create a new user with the appropriate name and email and a random password
			random_password = User.objects.make_random_password()
			new_user = User.objects.create_user(twitch_name, twitch_email, random_password)

			# take the data and attach it to the profile
			new_user.profile.twitch_id = twitch_id
			new_user.profile.twitch_refresh_token = twitch_refresh_token
			new_user.profile.twitch_OAuth_token = twitch_oauth_token
			new_user.profile.save(update_fields=['twitch_id'])
			new_user.profile.save(update_fields=['twitch_refresh_token'])
			new_user.profile.save(update_fields=['twitch_OAuth_token'])

			# log the new user in 
			emailer.email(new_user, "welcome")
			login(request, new_user)
			return 1
		except Exception as e:
			# failure to access actual user data
			return 0
	except:
		#failure on authenticating code from twitch
		return -1

# This is the Twitch Login function. It runs the normal Twitch auth cycle, 
# checks if the account is connected, and then logs them in
def login_with_twitch(request, code):
	try:
		# twitch auth step one. send back their code with our credentials to get user credentials
		twitch_client_id = config('TWITCH_LOGIN_CLIENT_ID')
		twitch_secret = config('TWITCH_LOGIN_SECRET')
		twitch_redirect_uri = config('TWITCH_LOGIN_REDIRECT_URI')
		headers = {
			'content-type': 'application/json',
			'Client-id': twitch_client_id
		}
		data = {
			"grant_type":"authorization_code",
			'client_id': twitch_client_id,
			"client_secret": twitch_secret,
			"code": code,
			"redirect_uri": twitch_redirect_uri
		}
		twitch_response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=json.dumps(data))
		twitch_dict=json.loads(twitch_response.text)
		context={}
		try:
			# Twitch auth step 2. send user credentials to get user data back
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
			response = requests.get('https://api.twitch.tv/kraken/user', headers=headers)
			twitch_dict2 = json.loads(response.text)
			print(twitch_dict2)
			twitch_id = twitch_dict2['_id']

			# Search for account
			try:
				logging_user_profile = UserProfile.objects.get(twitch_id=twitch_id)
				logging_user = logging_user_profile.user
			except Exception as e:
				return 2

			# take the data and attach it to the profile
			logging_user.profile.twitch_id = twitch_id
			logging_user.profile.twitch_refresh_token = twitch_refresh_token
			logging_user.profile.twitch_OAuth_token = twitch_oauth_token
			logging_user.profile.save(update_fields=['twitch_id'])
			logging_user.profile.save(update_fields=['twitch_refresh_token'])
			logging_user.profile.save(update_fields=['twitch_OAuth_token'])

			# log the  user in 
			print('about to log in')
			login(request, logging_user)
			print('logged in')
			return 1
		except Exception as e:
			# failure to access actual user data
			return 0
	except:
		#failure on authenticating code from twitch
		return -1


# def getOAuth(code, user_obj):
# 	print(1)
# 	headers = {
# 	    'content-type': 'application/json',
# 	    'Client-id': 'f054futox6ybt8p07bndbqbuaw0v48'
# 	}
# 	data = {"grant_type":"authorization_code",'client_id': 'f054futox6ybt8p07bndbqbuaw0v48',
# 	"client_secret": "anu2ub103e0or8had2cn1h3d6yxtld","code":
# 	code,"redirect_uri": "https://granite.gg/profiles/twitchauth/confirmation/"}
# 	twitch_response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=json.dumps(data))
# 	twitch_dict=json.loads(twitch_response.text)
# 	print(twitch_dict)
# 	return twitch_dict

# def getChannelInfo(OAuth):
# 	auth_string = 'OAuth '
# 	auth_string+= OAuth
# 	print(OAuth)
# 	headers = {
#         'Accept': 'application/vnd.twitchtv.v5+json',
#         'Client-ID': 'k6pbewo0iifuw2fu73rn9wz7k0beu1',
#         'Authorization': auth_string,
# 	}

# 	response = requests.get('https://api.twitch.tv/kraken/channel', headers=headers)
# 	return response

def is_twitch_sub(party_owner, party_joiner):
	print("Checking that ")
	print(party_joiner.username)
	print(party_joiner.profile.twitch_id)
	print("is subscribed to")
	print(party_owner.username)
	print(party_owner.profile.twitch_id)
	try:
		twitch_client_id = config('TWITCH_CLIENT_ID')
		twitch_secret = config('TWITCH_SECRET')
		twitch_redirect_uri = config('TWITCH_REDIRECT_URI')
		print(0)
		if party_owner.profile.twitch_id=="" or party_joiner.profile.twitch_id=="":
			return False
		print(1)
		auth_string = 'OAuth '
		auth_string+= party_owner.profile.twitch_OAuth_token
		headers = {'Accept': 'application/vnd.twitchtv.v5+json','Client-ID': twitch_client_id,'Authorization': auth_string,}
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
	except Exception as e:
		print(e)
		refresh_twitch_credentials(party_owner)
		print("EXCEPTION IN TWITCH SUB")
		return False



def refresh_twitch_credentials(user_obj):
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