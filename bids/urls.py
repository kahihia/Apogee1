
# from django.contrib import admin
# from django.urls import path, include, re_path
# from django.views.static import serve
# from django.views.generic.base import RedirectView
# from django.conf import settings
# from django.conf.urls.static import static

# from .views import (  
# 	BidListView, BidCreateView, BidUpdateView, BidDeleteView
# 	)
# from django.conf.urls import url
# app_name = 'bids'

# #Used for better understanding of MVC system of Django
# #Bid creation, retrieval, update, and deletion not available
# #to user directly anywhere

# #/bids routes to this
# urlpatterns = [
# 	path('list/', BidListView.as_view(), name='list'), #bids/
# 	path('', BidCreateView.as_view(), name='create'), #bids/create
# 	path('<int:pk>/update/', BidUpdateView.as_view(), name='update'), #bids/<int>/update
# 	path('<int:pk>/delete/', BidDeleteView.as_view(), name='delete') #bids/<int>/delete
# ]