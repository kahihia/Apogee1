from django import forms

from .models import Party

class PartyModelForm(forms.ModelForm):
	# the altered form fields are for formatting on the create page
	title = forms.CharField(label='', widget=forms.Textarea(
		attrs={'placeholder': 'Title', 'class': 'form-control'}
		))
	description = forms.CharField(label='', widget=forms.Textarea(
		attrs={'placeholder': 'Description', 'class': 'form-control'}
		))
	party_time = forms.SplitDateTimeField(label='', widget=forms.SplitDateTimeWidget(
		date_attrs={'placeholder': 'mm/dd/yy', 'class': 'form-control'}, 
		time_attrs={'placeholder': 'hh:mm 24 hr clock', 'class': 'form-control'}
		))
	class Meta:
		model = Party
		fields = [
			# 'user',
			'title',
			'description',
			'party_time'
		]

	# simple field validation
	# def clean_title(self, *args, **kwargs):
	# 	title = self.cleaned_data.get('title')
	# 	if title == 'poop':
	# 		raise forms.ValidationError('Cannot be poop')
	# 	return title