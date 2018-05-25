from django import forms
from .models import Bid

#bid model form for practice
#deprecated
class BidModelForm(forms.ModelForm):
	class Meta:
		model = Bid
		fields =[
			'bid_amount',
			'user',
			'party'
		]


	def clean_bid_amount(self, *args, **kwargs):
			bid_amount = self.cleaned_data.get('bid_amount')
			return bid_amount

# #bid model form for practice
# #deprecated
# class BidModelForm2(forms.ModelForm):
# 	class Meta:
# 		model = Bid
# 		fields =[
# 			'bid_amount',
# 			#'user',
# 			'party'
# 		]