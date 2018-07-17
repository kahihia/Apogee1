# forms determine what information is available in the create and update views
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Party
import boto3

class PartyModelForm(forms.ModelForm):
	# the altered form fields are for formatting on the create page
	# form-control allows bootstrap to format the form
	title = forms.CharField(label='', max_length=140, widget=forms.Textarea(
		attrs={'placeholder': 'Title', 'class': 'form-control', 'rows': 3}
		))
	description = forms.CharField(label='', max_length=280, widget=forms.Textarea(
		attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 7}
		))
	# localize tells us that this is in localtime so it converts to UTC for storage
	party_time = forms.SplitDateTimeField(label='', localize=True, widget=forms.SplitDateTimeWidget(
		date_attrs={'placeholder': 'Date: mm/dd/yy','type': 'date', 'class': 'form-control'}, 
		time_attrs={'placeholder': 'Time: hh:mm AM/PM or hh:mm 24-hr','type': 'time', 'class': 'form-control'}
		), input_time_formats=['%I:%M %p', '%H:%M', '%H:%M:%S'])

	# max_entrants = forms.ChoiceField(required=False, label='How many people can enter?',
	# 	widget=forms.Select(attrs={'class': 'form-control'}), 
	# 	choices=(
	# 			(None, 'Unlimited'), 
	# 			(10, 10), 
	# 			(25, 25), 
	# 			(50, 50), 
	# 			(100, 100), 
	# 			(500, 500), 
	# 			(1000, 1000)))

	num_possible_winners = forms.IntegerField(label='Number of possible winners', min_value=1, 
		widget=forms.NumberInput(attrs={'placeholder': 'Minimum of 1 winner', 'class': 'form-control'}))
	

	cost = forms.DecimalField(label='Cost ($)', min_value=0, widget=forms.NumberInput(
		attrs={'placeholder': 'For a FREE event, enter 0', 'class': 'form-control'}))

	thumbnail = forms.ImageField(label='Thumbnail')

	# event_type has a default widget so we're not gonna mess with it
	# event_type = forms.ChoiceField(label='Event Type')

	class Meta:
		model = Party
		# fields determines what order the form fields appear in
		fields = [
			'title',
			'description',
			'party_time',
			'event_type',
			'max_entrants', 
			'num_possible_winners', 
			'cost',
			'thumbnail', 
		]

		# dont think these will ever appear cause the fields have length limits on them 
		# like it just doesnt accept any more input after it hits the limit. 
		error_messages = {
            'title': {
                'max_length': "This title is too long.",
            },
            'description': {
                'max_length': "This description is too long.",
            },
        }

	# ensures that the event cannot be scheduled for the past. 
	def clean_party_time(self, *args, **kwargs):
		party_time = self.cleaned_data.get('party_time')
		if party_time < timezone.now():
			raise forms.ValidationError('Event cannot be in the past.')
		return party_time

	def clean_upload(self):
		print("clean_upload")
		upload = self.cleaned_data.get('thumbnail')
		s3 = boto3.resource('s3')
		s3.Bucket('apogee-assets').put_object(Key='test.jpg', Body=data)
	# ensures that the event cannot have more winners than entrants. 
	# has to be called on the second field because the second field isnt 
	# processed yet if its called on the first
	def clean_num_possible_winners(self, *args, **kwargs):
		max_entrants = self.cleaned_data.get('max_entrants')
		num_possible_winners = self.cleaned_data.get('num_possible_winners')
		if max_entrants is not None:
			if num_possible_winners > max_entrants:
				raise forms.ValidationError('Event cannot have more winners than entrants.')
		return num_possible_winners
		