# -*- coding: utf-8 -*-

from django.conf.urls import url
from trips.views import TripsListView, ViewTrip

__author__ = 'rafael'

urlpatterns = [

    url(r'^trip/(?P<trip_pk>\d+)/$', ViewTrip.as_view(),
        name='single_trip'),
    url(r'^list_trips/', TripsListView.as_view(), name="trips"),

]
