from django.core.mail import EmailMessage
from django.template.loader import get_template
from random import randint
from decouple import config
import json
import requests
import random
import string
from ast import literal_eval
from mailin import Mailin

# def email(subject, from_email, to_emails, template, email_data):
def email(user_obj, email_type):
	""" Utility email function
		* template: takes a the file name of a email template in the templates directory, email dir is appended already
		* kwargs: takes a object with keys appropriate to the message
	"""
	user_email = user_obj.email

	if config('EMAIL_ON', default=False, cast=bool):
		try:
			auth_token=""
			if True:
				auth_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
				user_obj.profile.email_auth_token = auth_token
				user_obj.profile.save(update_fields=['email_auth_token'])
			m = Mailin("https://api.sendinblue.com/v2.0", config('SENDINBLUE_V2_KEY'))
			data = { "to" : {user_email:"to whom!"},
				"from" : ["developers@apogee.gg", "Welcome to Granite!"],
				"subject" : "Account Authentication",
				"html" : "<h1>Welcome to Granite!</h1>\nYour account has been successfully registered!\n\
				 Please visit https://www.granite.gg/authentication and enter in <strong>"+auth_token+"</strong> to authenticate your account"
				}
			result = m.send_email(data)
		except:
			print("Email error")


	# if not config('EMAIL_ON'):
	# 	template = get_template('emails/' + template)
	# 	email_data['email'] = ''.join(to_emails)
	# 	html_content = template.render(email_data)
	# 	msg = EmailMessage(subject, html_content, 'Granite <' + from_email + '>', to_emails, headers={'Precedence': 'bulk'})
	# 	msg.content_subtype = "html"
	# 	msg.send()
	# else:
	# 	print("NoEmail")
	# a=3

