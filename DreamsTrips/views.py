# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import ListView
from profiles.models import Profile
from python_recipes import response_json

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


class DreamWorkersListView(ListView):
    """
        View for list of dreamworkers.
        Returns a list of trips along with their pic for the carousel
        back to the template for display
    """

    template_name = 'team.html'
    model = Profile
    paginate_by = 50
    user = None

    def get_queryset(self, **kwargs):
        print self.request.GET
        dream_workers = Profile.objects.filter(auth_user__is_active=1,
                                               is_dream_worker=1)

        self.user = self.request.user

        return dream_workers

    def get_context_data(self, **kwargs):
        context = super(DreamWorkersListView, self).get_context_data(**kwargs)

        return context


def send_contact_message(request):
    if request.method == "POST":
        comment = request.POST.get('comment', None)
        first_name = request.POST.get('comment', None)
        last_name = request.POST.get('comment', None)
        phone = request.POST.get('comment', None)
        email = request.POST.get('comment', None)


        message = first_name + last_name + phone + email + comment

        send_mail(
            'Web Page Comment',
            message,
            'rmoreno.ter@gmail.com',
            ['rmoreno.ter@gmail.com'],
            fail_silently=False,
        )

        return response_json('mail sent', 200)

    else:
        return response_json("Method not allowed", 409)


def send_quote_request(request):
    if request.method == "POST":
        comment = request.POST.get('comment', None)
        first_name = request.POST.get('comment', None)
        last_name = request.POST.get('comment', None)
        phone = request.POST.get('comment', None)
        email = request.POST.get('comment', None)

        message = first_name + last_name + phone + email + comment

        send_mail(
            'Cotization Request',
            message,
            'rmoreno.ter@gmail.com',
            ['rmoreno.ter@gmail.com'],
            fail_silently=False,
        )

        return response_json('mail sent', 200)

    else:
        return response_json("Method not allowed", 409)


def policy_view(request):
    reviews_list = []
    context = {'reviews': reviews_list, 'exp_pics': '',
               'request': request, 'user': request.user,
               'profile': '', 'experiences': ''}
    return render(request, 'trips_policy.html', context=context)
