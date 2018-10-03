from django.core.mail import EmailMessage
from django.template.loader import get_template
from random import randint
from decouple import config
import json
import requests
from ast import literal_eval

# def email(subject, from_email, to_emails, template, email_data):
def email(user_obj, email_type):
	""" Utility email function
		* template: takes a the file name of a email template in the templates directory, email dir is appended already
		* kwargs: takes a object with keys appropriate to the message
	"""
	user_email = user_obj.email
	print(user_email)
	# if email_type == "welcome":

	if config('EMAIL_ON', default=False, cast=bool):
		try:
			from mailin import Mailin
			print("_________________________________________________________________________--")
			m = Mailin("https://api.sendinblue.com/v2.0", config('SENDINBLUE_V2_KEY'))
			data = { "to" : {user_email:"to whom!"},
				"from" : ["developers@apogee.gg", "Welcome to Granite!"],
				"subject" : "Account Registration",
				"html" : "<h1>Welcome to Granite!</h1>\nYour account has been successfully registered!"
				}
			result = m.send_email(data)
			print(result)
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

