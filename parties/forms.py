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
	# localize tells us that this is in localtime so it converts to UTC for storage
	party_time = forms.SplitDateTimeField(label='', localize=True, widget=forms.SplitDateTimeWidget(
		date_attrs={'placeholder': 'Date: mm/dd/yy', 'class': 'form-control'}, 
		time_attrs={'placeholder': 'Time: hh:mm AM/PM or hh:mm 24-hr', 'class': 'form-control'}
		), input_time_formats=['%I:%M %p', '%H:%M'], help_text='specify AM or PM if using a 12 hour clock')
	class Meta:
		model = Party
		fields = [
			# 'user',
			'title',
			'description',
			'party_time', 
			'thumbnail'
		]

	# simple field validation
	# def clean_title(self, *args, **kwargs):
	# 	title = self.cleaned_data.get('title')
	# 	if title == 'poop':
	# 		raise forms.ValidationError('Cannot be poop')
	# 	return title