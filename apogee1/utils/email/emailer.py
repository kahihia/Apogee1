from django.core.mail import EmailMessage
from django.template.loader import get_template
from random import randint
from decouple import config

def email(subject, from_email, to_emails, template, email_data):
	""" Utility email function
		* template: takes a the file name of a email template in the templates directory, email dir is appended already
		* kwargs: takes a object with keys appropriate to the message
	"""
	if not config('EMAIL_ON'):
		template = get_template('emails/' + template)
		email_data['email'] = ''.join(to_emails)
		html_content = template.render(email_data)
		msg = EmailMessage(subject, html_content, 'Granite <' + from_email + '>', to_emails, headers={'Precedence': 'bulk'})
		msg.content_subtype = "html"
		msg.send()
	else:
		print("NoEmail")
	a=3

