from django import forms
#from .models import Bid, Party
from .models import Bid

class BidModelForm(forms.ModelForm):
	class Meta:
		model = Bid
		fields =[
			'bid_amount',
			'user',
			'party'
		]


	def clean_bid_amount(self, *args, **kwargs):
			bid = self.cleaned_data.get('bid_amount')
			#if bid < 0:
				#raise forms.ValidationError("INPUT ERROR: Bid cannot be less than 0")
			# try:
   # 				val = int(bid)
			# except ValueError:
   # 				raise forms.ValidationError("INPUT ERROR: Bid must be an integer")
			return bid
class BidModelForm2(forms.ModelForm):
	class Meta:
		model = Bid
		fields =[
			'bid_amount',
			#'user',
			'party'
		]