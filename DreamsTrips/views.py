# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView
from profiles.models import Profile

__author__ = 'root'


# @login_required(login_url='user_login')
def home_view(request):

    reviews_list = []

    context = {'reviews': reviews_list, 'exp_pics': '',
               'request': request, 'user': request.user,
               'profile': '', 'experiences': ''}
    return render(request, 'home.html', context=context)


def mission_view(request):
    reviews_list = []
    context = {'reviews': reviews_list, 'exp_pics': '',
               'request': request, 'user': request.user,
               'profile': '', 'experiences': ''}
    return render(request, 'mission.html', context=context)


def team_view(request):
    reviews_list = []

    context = {'reviews': reviews_list, 'exp_pics': '',
               'request': request, 'user': request.user,
               'profile': '', 'experiences': ''}
    return render(request, 'team.html', context=context)


class DreamworkersListView(ListView):
    """
        View for list of dreamworkers.
        Returns a list of trips along with their pic for the carousel
        back to the template for display
    """

    template_name = 'team.html'
    model = Profile
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
