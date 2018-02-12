from django import forms
from django.forms.utils import ErrorList

# this is for the update view. it ensures only the owner can edit
class ProfileOwnerMixin(object):
	def form_valid(self, form):
		if form.instance.user == self.request.user:
			return super(UserOwnerMixin, self).form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["You don't own this profile."])
			return self.form_invalid(form)
	