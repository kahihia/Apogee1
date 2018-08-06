# views tell us the templates and methods available to each page
# because this is the api, the views specify the action that happend upon visit
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from decimal import Decimal
import json

from parties import partyHandling
from bids.models import Bid
from parties.models import Party
from accounts.models import UserProfile
from .pagination import StandardResultsPagination
from .serializers import PartyModelSerializer
from paypalrestsdk.notifications import WebhookEvent
from decouple import config
import paypalrestsdk
paypal_api = paypalrestsdk.Api({
  'mode': 'sandbox',
  'client_id': 'AYVs-7u_YV5YGnV2c8q4L0i8Ke6iZjVwY6JoumipioAh-8do6ZHCC9sYP94PpS62ZTbdqVTCNV39h0uw',
  'client_secret': 'EBL0rnyKpDsbb5Tg657jVfJGU-uT8mDu8LuwbBucDAGEbAWu2-h59WMb7Uv6mcA1TtGH3gVwCoekOWJ_'})


class PaypalVerificationAPI(APIView):
	@csrf_exempt
	def post(self, request, format=None):
		# Paypal-Transmission-Id in webhook payload header
		transmission_id = request.META.get("HTTP_PAYPAL_TRANSMISSION_ID")
		# Paypal-Transmission-Time in webhook payload header
		timestamp =  request.META.get("HTTP_PAYPAL_TRANSMISSION_TIME")
		# Webhook id created
		webhook_id = config("WEBHOOK_ID", default="9EC012240A567735B")
		# Paypal-Transmission-Sig in webhook payload header
		actual_signature = request.META.get("HTTP_PAYPAL_TRANSMISSION_SIG") 
		# Paypal-Cert-Url in webhook payload header
		cert_url = request.META.get("HTTP_PAYPAL_CERT_URL")
		# PayPal-Auth-Algo in webhook payload header
		auth_algo = 'sha256'

		json_paypal = json.loads(request.body)		
		original_payment = paypalrestsdk.Payment.find(json_paypal['resource']['parent_payment'])
		user_id = original_payment['transactions'][0]['custom']
		u = UserProfile.objects.get(id=user_id)
		response = WebhookEvent.verify(transmission_id, timestamp, webhook_id, request.body.decode('utf-8'), cert_url, actual_signature, auth_algo)
		if response:
			payment = Decimal(original_payment['transactions'][0]['amount']['total'])
			u.account_balance = u.account_balance + payment
			u.save()

		return Response(response)

# star toggle is a method from the model that just adds the user to the 
# list containing the people who have starred it
class StarToggleAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, pk, format=None):
		# gets the object that is being starred
		party_qs = Party.objects.filter(pk=pk)
		if request.user.is_authenticated:
			is_starred = partyHandling.star_toggle(request.user, party_qs.first())
			return Response({'starred': is_starred})
			return Response({'message': 'Not Allowed'})

# join works much like star. its a method from the model. however, its
# built not to toggle. it only adds at the moment

#change this to handle all purchase types

class BidAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, pk, bids, format=None):
		print("The bid is: ")
		print(bids)
		party_qeryset = Party.objects.filter(pk=pk)
		party_event_type = party_qeryset.first().event_type
		#if party_event is bid	
		if party_event_type == 2:
			if request.user.is_authenticated:
				bid_table = partyHandling.bid_add(request.user, party_qeryset.first(), bids)
				return Response({'bid_accepted': bid_table["bid_accepted"],
								'min_bid': bid_table["min_bid"],
								'error_message':bid_table["error_message"]
								})




class BuyoutLotteryAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, pk, format=None):
		party_qeryset = Party.objects.filter(pk=pk)
		party_event_type = party_qeryset.first().event_type
		print('the party event type is: '+str(party_event_type))
		#if party_event is lottery
		if party_event_type == 1:
			if request.user.is_authenticated:
				joined_table = partyHandling.lottery_add(request.user, party_qeryset.first())
				return Response({'joined': joined_table["is_joined"],
								'num_joined':joined_table["num_joined"],
								'error_message':joined_table["error_message"]
								})
		#if party_event is buyout
		elif party_event_type == 2:
			return Response({'bid_accepted': False,
			'min_bid':party_qeryset.first().minimum_bid,
			'error_message':"Improper input"
			})
		else:
			if request.user.is_authenticated:
				buy_table = partyHandling.buyout_add(request.user, party_qeryset.first())
				return Response({'won':buy_table["winner"],
								'num_curr_winners':buy_table["num_winners"],
								'error_message':buy_table["error_message"]
								})

# used to async create events and push them to the api list
# so that we can update the main page with the new tweet
# CURRENTLY UNUSED
class PartyCreateAPIView(generics.CreateAPIView):
	serializer_class = PartyModelSerializer
	# ensures user is logged in to create
	permission_classes = [permissions.IsAuthenticated]

	# allows the api to create event with user data
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


# used for the single detail view. it searches the query on a single ID
class PartyDetailAPIView(generics.ListAPIView):
	queryset = Party.objects.all()
	serializer_class = PartyModelSerializer
	permission_classes = [permissions.AllowAny]
	pagination_class = StandardResultsPagination

	def get_queryset(self, *args, **kwargs):
		# these lists get the users you block and the users that block you
		# blocked by returns profile objects and blocking returns users
		blocked_by_list = self.request.user.blocked_by.all()
		party_id = self.kwargs.get('pk')
		qs = Party.objects.filter(pk=party_id)
		# this stops you from seeing blocked or blocking events
		qs = qs.exclude(user__profile__in=blocked_by_list)
		return qs


# this creates the api view that our search page pulls from
# it differs from the list view in that it includes users we arent following
class SearchPartyAPIView(generics.ListAPIView):
	queryset = Party.objects.all().order_by('-time_created')
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass the request into the serializer and get requestuser info
	def get_serializer_context(self, *args, **kwargs):
		context = super(SearchPartyAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	# this interacts with the call to this url
	def get_queryset(self, *args, **kwargs):		
		# this return the string form of the search passed into the url
		qs = self.queryset
		query = self.request.GET.get('q', None)
		if query is not None:
			# these lists get the users you block and the users that block you
			# blocked by returns profile objects and blocking returns users
			blocked_by_list = self.request.user.blocked_by.all()
			blocking_list = self.request.user.profile.blocking.all()
			# Q is a lookup function
			qs = qs.filter(
				Q(description__icontains=query) | 
				Q(user__username__icontains=query) | 
				Q(title__icontains=query)
				)
			# this stops you from seeing blocked or blocking events
			qs = qs.exclude(user__profile__in=blocked_by_list)
			qs = qs.exclude(user__in=blocking_list)
			qs = qs.filter(is_open=True).order_by('-popularity')
			return qs


# this creates the api view that our list pages pulls from
class PartyListAPIView(generics.ListAPIView):
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass the request into the serializer and get requestuser info
	def get_serializer_context(self, *args, **kwargs):
		context = super(PartyListAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	# this interacts with the ajax call to this url
	def get_queryset(self, *args, **kwargs):
		# gets user for if we have a user detail view
		requested_user = self.kwargs.get('username')
		# these lists get the users you block and the users that block you
		# blocked by returns profile objects and blocking returns users
		blocked_by_list = self.request.user.blocked_by.all()
		blocking_list = self.request.user.profile.blocking.all()
		if requested_user:
			# includes only the requested users events in the feed
			# sets the ordering. party_time would be soonest expiration at the top
			qs = Party.objects.filter(user__username=requested_user).order_by('-time_created')
			# this stops you from seeing blocked or blocking events
			qs = qs.exclude(user__profile__in=blocked_by_list)
			qs = qs.exclude(user__in=blocking_list)
		else:
			# uses methods form the userprofile model
			im_following = self.request.user.profile.get_following()
			qs = Party.objects.filter(user__in=im_following)
			qs = qs.filter(is_open=True).order_by('-time_created')
			# this stops you from seeing blocked or blocking events
			qs = qs.exclude(user__profile__in=blocked_by_list)
			qs = qs.exclude(user__in=blocking_list)
			# includes our own events in our feed
			# qs2 = Party.objects.filter(user=self.request.user)
			# sets the ordering. party_time would be soonest expiration at the top
			# qs = (qs1 | qs2).distinct().order_by('-time_created')

		# this return the string form of the search passed into the url
		# currentyl all search goes to the search api view, not this
		# query = self.request.GET.get('q', None)
		# if query is not None:
		# 	# Q is a lookup function
		# 	qs = qs.filter(
		# 		Q(description__icontains=query) | 
		# 		Q(user__username__icontains=query) | 
		# 		Q(title__icontains=query)
		# 		)
		return qs



# this creates the api view that our starred list page pulls from
class StarredListAPIView(generics.ListAPIView):
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass the request into the serializer and get requestuser info
	def get_serializer_context(self, *args, **kwargs):
		context = super(StarredListAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	# this interacts with the ajax call to this url
	def get_queryset(self, *args, **kwargs):
		# these lists get the users you block and the users that block you
		# blocked by returns profile objects and blocking returns users
		blocked_by_list = self.request.user.blocked_by.all()
		blocking_list = self.request.user.profile.blocking.all()
		qs = self.request.user.starred_by.all().order_by('-time_created')
		# this stops you from seeing blocked or blocking events
		qs = qs.exclude(user__profile__in=blocked_by_list)
		qs = qs.exclude(user__in=blocking_list)
		return qs

# this works the same way as the starred list
class JoinedListAPIView(generics.ListAPIView):
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass the request into the serializer and get requestuser info
	def get_serializer_context(self, *args, **kwargs):
		context = super(JoinedListAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	# this interacts with the ajax call to this url
	def get_queryset(self, *args, **kwargs):
		# these lists get the users you block and the users that block you
		# blocked by returns profile objects and blocking returns users
		blocked_by_list = self.request.user.blocked_by.all()
		blocking_list = self.request.user.profile.blocking.all()
		qs = self.request.user.joined_by.all().order_by('-time_created')
		# this stops you from seeing blocked or blocking events
		qs = qs.exclude(user__profile__in=blocked_by_list)
		qs = qs.exclude(user__in=blocking_list)
		return qs


# this creates the api view that the trending list of our home page pulls from
class TrendingListAPIView(generics.ListAPIView):
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass the request into the serializer and get requestuser info
	def get_serializer_context(self, *args, **kwargs):
		context = super(TrendingListAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	# this interacts with the ajax call to this url
	def get_queryset(self, *args, **kwargs):
		# these lists get the users you block and the users that block you
		# blocked by returns profile objects and blocking returns users
		blocked_by_list = self.request.user.blocked_by.all()
		blocking_list = self.request.user.profile.blocking.all()
		# trending is all the open events, ordered by their popularity, descending
		qs = Party.objects.filter(is_open=True).order_by('-popularity')
		qs = qs.exclude(user__profile__in=blocked_by_list)
		qs = qs.exclude(user__in=blocking_list)
		return qs

# this creates the api view that the closing soon list of our home page pulls from
class ClosingSoonListAPIView(generics.ListAPIView):
	serializer_class = PartyModelSerializer
	pagination_class = StandardResultsPagination

	# this allows us to pass the request into the serializer and get requestuser info
	def get_serializer_context(self, *args, **kwargs):
		context = super(ClosingSoonListAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	# this interacts with the ajax call to this url
	def get_queryset(self, *args, **kwargs):
		# these lists get the users you block and the users that block you
		# blocked by returns profile objects and blocking returns users
		blocked_by_list = self.request.user.blocked_by.all()
		blocking_list = self.request.user.profile.blocking.all()
		# closing soon is events closing in 5 mins (delta is 10)
		# that are open, ordered by popularity, descending
		soon_time = timezone.now() + timedelta(minutes=15)
		qs = Party.objects.filter(is_open=True)
		qs = qs.filter(party_time__lte=soon_time)
		qs = qs.exclude(user__profile__in=blocked_by_list)
		qs = qs.exclude(user__in=blocking_list)
		qs = qs.order_by('-popularity')
		return qs





		