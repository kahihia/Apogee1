# validators are extra layers of security

from django.core.exceptions import ValidationError


# custom validation function for the create form
# currently not used
def validate_title(value):
	title = value
	if title == '':
		raise ValidationError('Title cannot be blank')
	return value


# we need a validator to ensure that the events are not in the past
# def validate_party_time(value):
# 	time = value
# 	if time - timezone.now < 0:
# 		raise ValidationError('Event must be in the future')
# 	return value