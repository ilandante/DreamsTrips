# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Role(models.Model):
    role = models.CharField(
        max_length=45,
        verbose_name='Rol'
    )

    def __str__(self):
        return self.role


@python_2_unicode_compatible
class Operation(models.Model):
    operation = models.CharField(
        max_length=45,
        verbose_name='Operación'
    )

    def __str__(self):
        return self.operation


class Object(models.Model):
    obj = models.CharField(
        max_length=45,
        verbose_name='Objeto'
    )

    def __str__(self):
        return self.obj


@python_2_unicode_compatible
class UserRole(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Usuario'
    )

    role = models.ForeignKey(
        Role, on_delete=models.CASCADE,
        verbose_name='Rol'
    )

    status = models.BooleanField(
        default=True,
        verbose_name='Estado'
    )

    def __str__(self):
        return '%s es %s' % (
            self.user.username,
            self.role
        )


@python_2_unicode_compatible
class PermissonAssignment(models.Model):
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE,
        verbose_name='Rol'
    )

    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE,
        verbose_name='Operación'
    )

    obj = models.ForeignKey(
        Object, on_delete=models.CASCADE,
        verbose_name='Objeto'
    )

    def __str__(self):
        return '%s puede %s %s' % (
            self.role,
            self.operation,
            self.obj
        )
