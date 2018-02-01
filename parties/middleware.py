import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

# this is the local timezone activation method from the django docs
class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
            # print('activated')
        else:
            timezone.deactivate()
            # print('not activated')