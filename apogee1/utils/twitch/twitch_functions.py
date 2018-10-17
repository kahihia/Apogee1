import requests

def getOAuth(code):
	headers = {
	    'content-type': 'application/json',
	    'Client-id': 'f054futox6ybt8p07bndbqbuaw0v48'
	}
	data = {"grant_type":"authorization_code",'client_id': 'f054futox6ybt8p07bndbqbuaw0v48',
	"client_secret": "anu2ub103e0or8had2cn1h3d6yxtld","code":
	code,"redirect_uri": "https://malek-server.herokuapp.com/profiles/Tes/twitchauth/"}
	twitch_response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=json.dumps(data))
	twitch_dict=json.loads(twitch_response.text)
	return twitch_dict

def getChannelInfo(OAuth):
	auth_string = 'OAuth '
	auth_string+= OAuth
	print(OAuth)
	headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': 'f054futox6ybt8p07bndbqbuaw0v48',
        'Authorization': auth_string,
	}

	response = requests.get('https://api.twitch.tv/kraken/channel', headers=headers)
	return response