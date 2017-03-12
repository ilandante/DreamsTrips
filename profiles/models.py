# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from finances.models import Bank
from locations.models import City

__author__ = 'rafa'


@python_2_unicode_compatible
class Address(models.Model):
    city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        verbose_name='Ciudad'
    )

    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE,
        verbose_name='Perfil de usuario', blank=True, null=True
    )

    address = models.CharField(
        max_length=145,
        verbose_name='Dirección'
    )

    zipcode = models.CharField(
        blank=True, null=True,
        max_length=8,
        verbose_name='Código postal'
    )

    latitude = models.CharField(
        blank=True, null=True,
        max_length=32,
        verbose_name='Latitud'
    )

    longitude = models.CharField(
        blank=True, null=True,
        max_length=32,
        verbose_name='Longitud'
    )

    def __str__(self):
        return '%s, %s, %s' % (
            self.address,
            self.zipcode,
            self.city
        )


# TODO: Assign admin/dreamer
@python_2_unicode_compatible
class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'M'),
        ('F', 'F'))

    auth_user = models.ForeignKey(User,
                                  verbose_name='usuario')

    dream_worker = models.ForeignKey("Profile",
                                     related_name='assigned_dreamworker_profile',
                                     null=True, blank=True)

    phone = models.CharField(max_length=45,
                             verbose_name="número de telefono",
                             blank=True, null=True)

    birthday = models.DateField(verbose_name='fecha de nacimiento',
                                blank=True,
                                null=True)

    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              blank=True,
                              null=True,
                              verbose_name="género")

    profile_pic = models.FileField(upload_to='pofile_pictures',
                                   null=True,
                                   blank=True,
                                   verbose_name='imagen de perfil')

    observations = models.TextField(verbose_name='observaciones',
                                    blank=True,
                                    null=True)

    curp = models.CharField(max_length=45,
                            null=True,
                            blank=True,
                            verbose_name='CURP')

    rfc = models.CharField(max_length=45,
                           null=True,
                           blank=True,
                           verbose_name='RFC')

    ib_key = models.CharField(max_length=45,
                              null=True,
                              blank=True,
                              verbose_name='clave inerbancaria')

    destination_bank = models.ForeignKey('finances.Bank',
                                         verbose_name='banco de destino',
                                         null=True,
                                         blank=True,
                                         )

    is_dream_worker = models.BooleanField(default=0, verbose_name='es DreamWorker')

    def __str__(self):
        return self.auth_user.get_full_name()


@python_2_unicode_compatible
class DocumentType(models.Model):
    name = models.CharField(max_length=64,
                            verbose_name='nombre')
    description = models.CharField(max_length=200,
                                   verbose_name='descripción', blank=True,
                                   null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ClientDocument(models.Model):
    document = models.FileField(upload_to='client_files',
                                verbose_name='archivo')
    document_type = models.ForeignKey(DocumentType,
                                      verbose_name='Documento', blank=True,
                                      null=True)
    profile = models.ForeignKey(Profile, verbose_name='Perfil')
    file_name = models.CharField(max_length=128,
                                 verbose_name='Nombre del documento',
                                 blank=True, null=True)

    def __str__(self):
        return self.file_name
