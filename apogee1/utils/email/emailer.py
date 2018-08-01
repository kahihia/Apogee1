from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

def email(subject, from_email, to_emails, template, email_data):
	""" Utility email function
		* template: takes a the file name of a email template in the templates directory, email dir is appended already
		* kwargs: takes a object with keys appropriate to the message
	"""
	template = get_template('emails/' + template)
	html_content = template.render(email_data)
	text_content = 'Your mail client does not support HTML, you should probably move to one that does! In the meantime you have important messages on Apogee.'
	msg = EmailMultiAlternatives(subject, html_content, from_email, [to_emails])
	msg.attach_alternative(text_content, "text/plain")
	msg.send()
