# validators are extra layers of security

from django.core.exceptions import ValidationError


# custom validation function for the create form
# currently not used
def validate_title(value):
	title = value
	if title == '':
		raise ValidationError('Title cannot be blank')
	return value

def validate_profanity(value):
	content = value
	if is_profane(content):
		raise ValidationError('Please remove offensive language')


def is_profane(content):
	with open('profanity.txt', 'r') as myfile:
		words=myfile.readlines()
		words = [line.rstrip('\n') for line in words]
	for word in words:
		if word.lower() in content:
			return True
	return False


# we need a validator to ensure that the events are not in the past
# def validate_party_time(value):
# 	time = value
# 	if time - timezone.now < 0:
# 		raise ValidationError('Event must be in the future')
# 	return value