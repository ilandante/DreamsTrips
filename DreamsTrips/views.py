# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from profiles.models import Profile
from python_recipes import response_json
from trips.models import GalleryImage, TripGallery

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
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)

        message = 'Nombre: ' +first_name + ' Apellido: ' +last_name + ' Telefono: ' +\
                  phone + ' email: ' +email + ' Comentario: ' +comment

        send_mail(
            'Web Page Comment',
            message,
            'yoviajocondreamstrips@gmail.com',
            ['yoviajocondreamstrips@gmail.com'],
            fail_silently=False,
        )

        return response_json('mail sent', 200)

    else:
        return response_json("Method not allowed", 409)


def send_quote_request(request):
    if request.method == "POST":
        comment = request.POST.get('comment', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)

        message = 'Nombre: ' +first_name + ' Apellido: ' +last_name + ' Telefono: ' +\
                  phone + ' email: ' +email + ' Comentario: ' +comment

        send_mail(
            'Cotization Request',
            message,
            'yoviajocondreamstrips@gmail.com',
            ['yoviajocondreamstrips@gmail.com'],
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


class GalleryListView(ListView):
    """
        View for list of dreamworkers.
        Returns a list of trips along with their pic for the carousel
        back to the template for display
    """

    template_name = 'gallery.html'
    model = GalleryImage
    paginate_by = 50
    user = None

    def get_queryset(self, **kwargs):
        print self.request.GET
        images = TripGallery.objects.filter()

        self.user = self.request.user
        return images

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)

        return context


class ViewGallery(ListView):

    template_name = 'single_trip_gallery.html'
    pk = None
    trip = None
    user = None
    gallery = None

    def get_queryset(self, **kwargs):

        pk = self.kwargs.get('gallery_pk', None)

        if pk is not None:
            gallery = GalleryImage.objects.filter(gallery__pk=pk)
        else:
            raise AttributeError("PK No Encontrado")
        print gallery, 'find somethng!'
        return gallery

    def get_context_data(self, **kwargs):
        context = super(ViewGallery, self).get_context_data(**kwargs)
        return context
