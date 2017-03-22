# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from timezone_utils.fields import TimeZoneField
from timezone_utils.choices import PRETTY_ALL_TIMEZONES_CHOICES
from locations.models import City
from profiles.models import Profile

__author__ = 'rafa'


@python_2_unicode_compatible
class Trip(models.Model):
    title = models.CharField(max_length=45,
                             verbose_name='nombre del viaje')

    active = models.BooleanField(default=True)

    init_date = models.DateTimeField(null=True, blank=True,
                                     verbose_name="fecha inicial")

    end_date = models.DateTimeField(null=True, blank=True,
                                    verbose_name="fecha Final")

    origin_city = models.ForeignKey(City,
                                    null=True,
                                    blank=True,
                                    verbose_name="Ciudad")

    destination_city = models.ForeignKey(City,
                                         null=True,
                                         blank=True,
                                         related_name="destination",
                                         verbose_name="destino")

    description = models.TextField(verbose_name='descripción',
                                   blank=True,
                                   null=True)

    origin_timezone = TimeZoneField(choices=PRETTY_ALL_TIMEZONES_CHOICES,
                                    default='America/Mexico_City', blank=True,
                                    null=True)

    destination_timezone = TimeZoneField(choices=PRETTY_ALL_TIMEZONES_CHOICES,
                                         default='America/Mexico_City',
                                         blank=True,
                                         null=True)

    price_per_person = models.DecimalField(max_digits=20,
                                           decimal_places=2,
                                           verbose_name="precio por persona",
                                           null=True,
                                           blank=True)

    seats_available = models.PositiveIntegerField(verbose_name='asientos disponibles')

    private = models.BooleanField(default=False,
                                  verbose_name='viaje privado')

    kids_allowed = models.BooleanField(default=False,
                                       verbose_name='niños')

    photograph = models.ImageField(upload_to='galleries', blank=True, null=True)

    circle_photograph = models.ImageField(upload_to='galleries', blank=True,
                                          null=True)

    itinerary_file = models.FileField(upload_to='trip_files', blank=True,
                                      null=True, verbose_name='itinerario')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Itinerary(models.Model):
    name = models.CharField(max_length=64,
                            verbose_name='nombre')
    description = models.CharField(max_length=200,
                                   verbose_name='descripción')
    trip = models.ForeignKey(Trip, verbose_name='viaje')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ItineraryItem(models.Model):
    title = models.CharField(max_length=64,
                             verbose_name='title')

    init_date = models.DateTimeField(null=True, blank=True,
                                     verbose_name="fecha Inicial")

    end_date = models.DateTimeField(null=True, blank=True,
                                    verbose_name="fecha Final")

    description = models.CharField(max_length=200,
                                   verbose_name='Descripción')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ClientTrip(models.Model):
    GENDER_CHOICES = (
        ('D', 'Paid'),
        ('P', 'Pending'))

    trip = models.ForeignKey(Trip, verbose_name='viaje')

    client = models.ForeignKey(Profile, verbose_name='cliente')

    num_persons = models.PositiveIntegerField(verbose_name='numero de viajeros')

    pending_payment = models.PositiveIntegerField(verbose_name='suma pendiente',
                                                  blank=True,
                                                  null=True)
    registration_date = models.DateTimeField(null=True,
                                             blank=True,
                                             verbose_name="fecha inicial")

    def __str__(self):
        return self.trip.title + ' de ' + self.client.auth_user.get_full_name()


@python_2_unicode_compatible
class DocumentType(models.Model):
    name = models.CharField(max_length=64,
                            verbose_name='nombre')
    description = models.CharField(max_length=200,
                                   verbose_name='descripción')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TripGallery(models.Model):
    trip = models.ForeignKey(Trip, verbose_name='viaje')
    main_photo = models.FileField(upload_to='galleries')

    def __str__(self):
        return self.trip.title


@python_2_unicode_compatible
class GalleryImage(models.Model):
    gallery = models.ForeignKey(TripGallery, verbose_name='galeria',
                                blank=True, null=True)

    photograph = models.FileField(upload_to='galleries')

    def __str__(self):
        return self.photograph.url