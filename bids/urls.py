
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

from .views import (  BidListView
	)
from django.conf.urls import url
app_name = 'bids'

#/bids routes to this
urlpatterns = [
	path('', BidListView.as_view(), name='list'),
]