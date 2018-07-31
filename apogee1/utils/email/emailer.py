from django.core.mail import EmailMultiAlternatives

def email(subject, from_email, to_emails, template, **kwargs):
	""" Utility email function
		* template: takes a the file name of a email template in the templates directory, email dir is appended already
		* kwargs: takes a object with keys appropriate to the message
	"""
	template = get_template(template)
	c = Context(kwargs)
	html_content = template.render(c)

	msg = EmailMultiAlternatives(subject, template, from_email, to_emails, fail_silently=False)
	html_content = template.render(d)
	msg.attach_alternative(html_content, "text/html")
	msg.send()