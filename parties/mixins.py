from django import forms
from django.forms.utils import ErrorList

# this mixin is for the create view. it ensures that the
# user is logged in before the create request gets pushed
class FormUserNeededMixin(object):
	def form_valid(self, form):
		if self.request.user.is_authenticated:
			# pulls object from the form
			form.instance.user = self.request.user
			return super(FormUserNeededMixin, self).form_valid(form)
		else:
			# doesn't throw an error, but doesn't pass the form through
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(['User must be logged in to continue.'])
			return self.form_invalid(form)

# this is for the update view. it ensures only the owner can edit
class UserOwnerMixin(object):
	def form_valid(self, form):
		if form.instance.user == self.request.user:
			return super(UserOwnerMixin, self).form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["You don't own this event."])
			return self.form_invalid(form)
	