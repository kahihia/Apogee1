from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import UserProfile

User = get_user_model()

# these are the fields for building users
class UserRegisterForm(forms.Form):
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

	# this makes sure the passwords match
	def clean_password2(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError('Passwords must match.')
		return password

	# ensures the username doesnt already exist
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__icontains=username).exists():
			raise forms.ValidationError('This username is taken :(')
		return username

	# ensures the email doesnt already have an associated account
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email__icontains=email).exists():
			raise forms.ValidationError('This email is already in use')
		return email	


# for the user's profile
class UserProfileModelForm(forms.ModelForm):
	# the altered form fields are for formatting on the create page
	bio = forms.CharField(label='', required=False, widget=forms.Textarea(
		attrs={'placeholder': 'Bio', 'class': 'form-control', 'rows': 3}
		), help_text='Feel free to share as much or as little as you like. Personal history, games you like to play, etc.')
	
	profile_picture = forms.ImageField(label='Profile Picture', required=False)

	banner = forms.ImageField(label='Banner/cover photo', required=False)

	class Meta:
		model = UserProfile
		fields = [
			'bio',
			'profile_picture',
			'banner', 
		]

	
	


