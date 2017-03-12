# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from locations.models import City
# from profiles.models import Profile
# from trips.models import Trip

__author__ = 'rafa'


@python_2_unicode_compatible
class Quote(models.Model):

    user = models.ForeignKey(User,
                             verbose_name='usuario',
                             blank=True,
                             null=True)

    agent = models.ForeignKey(User,
                              related_name='agent',
                              verbose_name='agente',
                              blank=True,
                              null=True)

    num_persons = models.PositiveIntegerField(verbose_name='viajantes',
                                              default=1)

    destination = models.ForeignKey(City,
                                    verbose_name='destino',
                                    blank=True,
                                    null=True)

    written_destination = models.CharField(max_length=45,
                                           verbose_name='destino')

    details = models.TextField(verbose_name='detalles')

    init_date = models.DateTimeField(null=True,
                                     blank=True,
                                     verbose_name="fecha inicial")

    end_date = models.DateTimeField(null=True,
                                    blank=True,
                                    verbose_name="fecha Final")

    request_date = models.DateTimeField(null=True,
                                        blank=True,
                                        verbose_name="fecha Final")

    agency_price = models.PositiveIntegerField(verbose_name='precio de la agencia')

    email = models.EmailField(verbose_name='email',
                              blank=True,
                              null=True)

    def __str__(self):
        return self.auth_user.get_full_name()


@python_2_unicode_compatible
class Bank(models.Model):
    name = models.CharField(max_length=64,
                            verbose_name='nombre')
    description = models.CharField(max_length=200,
                                   verbose_name='descripción')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class UserPayment(models.Model):
    client = models.ForeignKey('profiles.Profile', verbose_name='cliente')

    quantity = models.PositiveIntegerField(verbose_name='cantidad')

    trip = models.ForeignKey('trips.Trip', verbose_name='viaje')

    payment_file = models.FileField(blank=True,
                                    null=True,
                                    verbose_name='archivo')
    registration_date = models.DateTimeField(null=True,
                                             blank=True,
                                             verbose_name="fecha de registro")

    def __str__(self):
        return self.client.auth_user.get_full_name() + ' ' + self.quantity