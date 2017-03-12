# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from profiles.models import Profile
from python_recipes import response_json
from trips.models import Trip, TripGallery, GalleryImage, Itinerary, \
    ItineraryItem
from django.core.mail import send_mail

__author__ = 'rafa'


class TripsListView(ListView):
    """
        View for list of trips.
        Returns a list of trips along with their pic for the carousel
        back to the template for display
    """

    template_name = 'group_trip_selector.html'
    model = Trip
    paginate_by = 50
    user = None
    trips = None

    def get_queryset(self, **kwargs):
        print self.request.GET
        trip = Trip.objects.filter(active=1)

        self.trips = trip
        self.user = self.request.user

        return trip

    def get_context_data(self, **kwargs):
        context = super(TripsListView, self).get_context_data(**kwargs)

        # context['experiences'] = self.trips

        return context


class ViewTrip(DetailView):
    """
    Detail view for a single experience. Returns the single experience, as well
    as the images related to that experience, other experiences by the same
    host, the activities related to the single experience and the pertaining
    reviews.
    """
    template_name = 'group_trip_detail.html'
    pk = None
    trip = None
    user = None
    profile = None

    def get_object(self, queryset=None):
        try:
            self.user = self.request.user
            self.profile = Profile.objects.get(auth_user=self.user)
        except:
            print "No user"
        self.pk = self.kwargs.get('trip_pk', None)

        if self.pk is not None:
            self.trip = Trip.objects.get(pk=self.pk)
        else:
            raise AttributeError("PK No Encontrado")
        return self.trip

    def get_context_data(self, **kwargs):
        context = super(ViewTrip, self).get_context_data(**kwargs)
        try:
            itinerary = Itinerary.objects.get(trip=self.trip)
            itinerary_items = ItineraryItem.objects.filter(itinerary=itinerary)
        except:
            itinerary_items = None

        try:
            gallery = TripGallery.objects.get(trip=self.trip)
            pics = GalleryImage.objects.filter(gallery=gallery)
        except:
            print "No gallery"
            pics = None

        context['trip_pics'] = pics
        context['trip'] = self.trip
        context['itinerary_items'] = itinerary_items

        return context


def send_comment(request, hosting_pk):
    if request.method == "POST":
        message = request.POST.get('comment', None)

        # send_mail(
        #     'Web Page Comment',
        #     message,
        #     'rafasylver@hotmail.com',
        #     ['rafasylver@hotmail.com.com'],
        #     fail_silently=False,
        # )

        return response_json('mail sent', 200)

    else:
        return response_json("Method not allowed", 409)