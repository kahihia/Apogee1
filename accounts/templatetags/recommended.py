from django import template
from django.contrib.auth import get_user_model

from accounts.models import UserProfile


register = template.Library()

User = get_user_model()

# this allows us to include chunks of code wherever we need

# this is our decorator
@register.inclusion_tag('accounts/snippets/recommended.html')

def recommended(user):
	# ensures that this is a user model
	if isinstance(user, User):
		# returns a qs identical to the one in the user model
		qs = UserProfile.objects.recommended(user)
		return {'recommended': qs}