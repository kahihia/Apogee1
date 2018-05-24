# from django.forms.utils import ErrorList
# from django import forms

# class FormUserNeededMixin(object):
# 	def form_valid(self, form):
# 		if self.request.user.is_authenticated:
# 			form.instance.user = self.request.user
# 			return super(FormUserNeededMixin, self).form_valid(form)
# 		else:
# 			form.errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["Log in to continue"])
# 			return self.form_invalid(form)


# class UserOwnerMixin(object):
# 	def form_valid(self, form):
# 		if self.request.user == form.instance.user:
# 			return super(UserOwnerMixin, self).form_valid(form)
# 		else:
# 			form.errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["Must be owner of bid to update"])
# 			return self.form_invalid(form)

