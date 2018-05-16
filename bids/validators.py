from django.core.exceptions import ValidationError

def validate_bid_amount(value):
	bid_amount = value
	if bid_amount<0:
		raise ValidationError("CONTENT ERROR: Bid amount cannot be less than 0")
	return value