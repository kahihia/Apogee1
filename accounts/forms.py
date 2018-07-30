from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from .models import UserProfile
from django.core.mail import send_mail

# this is the base user model in django
User = get_user_model()

# these are the fields for building users 
class UserRegisterForm(forms.Form):
	# because this is a regular form, not a modelform, it doesnt need the fields 
	# explicitly declared
	username = forms.CharField()
	email = forms.EmailField()
	# the two passwords are used for verification to make sure you didnt mistype
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


	# The following methods trigger on submit. howeer, they are triggered
	# before the form submits to the database. it's an inbetween step

	# this makes sure the passwords match
	def clean_password2(self):
		send_mail('Subject here', 'Here is the message.', 'apogee@apogee.gg', ['malek@apogee.gg'], fail_silently=False)
		# validation errors block the submit and return back to the register form
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if len(password) < 7:
			raise forms.ValidationError('Passwords must be at least 8 characters.')
		# first_isalpha = password1[0].isalpha()
  #       if all(c.isalpha() == first_isalpha for c in password1):
  #           raise forms.ValidationError('Password must contain one letter and one number.')
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


# These are the fields for editing a user profile
class UserProfileModelForm(forms.ModelForm):
	# the altered form fields are for formatting on the create page
	bio = forms.CharField(label='', required=False, widget=forms.Textarea(
		attrs={'placeholder': 'Bio', 'class': 'form-control', 'rows': 3}
		), help_text='Feel free to share as much or as little as you like. Personal history, games you like to play, etc.')
	
	# ImageFields have a url associated with them by default
	profile_picture = forms.ImageField(label='Profile Picture', required=False)

	banner = forms.ImageField(label='Banner/cover photo', required=False)

	# this tells the form what fields to actually display
	class Meta:
		model = UserProfile
		fields = [
			'bio',
			'profile_picture',
			'banner', 
		]

	
	


