from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from placesapi import views

urlpatterns = [
    path('search', views.Search.as_view(), name='search'),
    path('details/<slug:xid>', views.Details.as_view(), name='details')
]

urlpatterns = format_suffix_patterns(urlpatterns)
