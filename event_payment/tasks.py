from .models import EventPayment

def pay_owner(payment_id):
	try:
		# gets the correct payment
		# filter would return a queryset, we want an object.
		payment = EventPayment.objects.get(pk=payment_id)
	except EventPayment.DoesNotExist:
		# if the payment is deleted, it does nothing; TODO: Hook email notifications into delete action somewhere else
		return 
	if not payment.is_paid:
		owner = payment.payment_user
		amount_owed = payment.payment_amount
		curr_balance = owner.profile.account_balance + amount_owed
		owner.profile.account_balance = curr_balance
		owner.profile.save(update_fields=['account_balance'])
		payment.is_paid = True
		payment.save(update_fields=['is_paid'])