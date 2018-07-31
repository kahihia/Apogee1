from django import forms
from django.forms.utils import ErrorList

# mixins are methods you can use on views to ensure particular conditions are met

# this is for the profile update view. it ensures only the owner can edit
class ProfileOwnerMixin(object):
	# form valid is the default name for the validation methods that are part of the mixin
	def form_valid(self, form):
		# if the user is the profile owner, the form is validated
		if form.instance.user == self.request.user:
			return super(ProfileOwnerMixin, self).form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["You don't own this profile."])
			return self.form_invalid(form)
	