# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

__author__ = 'rafa'


@python_2_unicode_compatible
class Country(models.Model):
    name = models.CharField(max_length=64, verbose_name="país")
    sortname = models.CharField(max_length=5,
                                verbose_name='identificador', null=True,
                                blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class State(models.Model):
    name = models.CharField(max_length=64, blank=True,
                            null=True, verbose_name="Estado")
    country = models.ForeignKey(Country,
                                verbose_name="Pais",
                                related_name='countries')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(max_length=64, blank=True,
                            null=True, verbose_name="Ciudad")
    state = models.ForeignKey(State, verbose_name="Estado",
                              related_name='states', null=True,
                              blank=True)
    country = models.ForeignKey(Country, verbose_name="País", null=True,
                                blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AirPort(models.Model):
    name = models.CharField(max_length=128, blank=True,
                            null=True, verbose_name="Nombre")
    city = models.ForeignKey(City, verbose_name="Ciudad")
    identifier = models.CharField(max_length=5, null=True, blank=True,
                                  verbose_name='IATA')

    def __str__(self):
        return self.name
