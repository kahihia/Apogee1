from .models import EventPayment
from celery import shared_task

@shared_task
def pay_owner(payment_id):
	print("_______________________________________________________RUNNING PAYMENT______________")
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
		payment.save2(update_fields=['is_paid'])