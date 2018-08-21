# forms determine what information is available in the create and update views
from django import forms
#from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Payout

class PayoutModelForm(forms.ModelForm):
	# the altered form fields are for formatting on the create page
	# form-control allows bootstrap to format the form
	payment_info = forms.CharField(label='', max_length=140, widget=forms.Textarea(
		attrs={'placeholder': 'Payment info, ex: paypal account', 'class': 'form-control', 'rows': 1}
		))
	description = forms.CharField(label='', max_length=280, widget=forms.Textarea(
		attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 3}
		))


	class Meta:
		model = Payout
		# fields determines what order the form fields appear in
		fields = [
			'payment_info',
			'description',
		]

		# dont think these will ever appear cause the fields have length limits on them 
		# like it just doesnt accept any more input after it hits the limit. 
		error_messages = {
            'payment_info': {
                'max_length': "your payment_info is too long.",
            },
            'description': {
                'max_length': "This description is too long.",
            },
        }
	def clean_account_balance(self, request):
		user = self.instance.payout_user
		if user.profile.account_balance < 100:
			raise forms.ValidationError("You must have $100 in your account to request a payout")
