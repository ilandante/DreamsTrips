# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from rbac.models import PermissonAssignment, UserRole, Operation

__author__ = 'velocidad'


def check_roles_permission(object_name):
    """ Check the roles that have an allowed operation over an object
    :param object_name: string, the name of the object
    :return an array with a dict with keys: role and operation
    """
    permissions = PermissonAssignment.objects.filter(
        object__object=object_name)
    role_operations = []
    for perm in permissions:
        r_o = dict(role=perm.role, operation=perm.operation)
        role_operations.append(r_o)
    return role_operations


def has_permission(user, operation, object_name):
    """ Checks if a user has certain permission over an object

    :param user: django auth user object
    :param operation:  rbac operation object
    :param object_name: string, the name of the subject
    :return Boolean, true if the user has permission, False if not
    """
    user_role = UserRole.objects.filter(
        user=user, role__status='active').exclude(status=False)
    for u_role in user_role:
        permission = PermissonAssignment.objects.filter(
            object__object=object_name,
            role=u_role.role, operation=operation)
        if permission:
            return True
    return False


def has_permission_str(user, operation, object_name):
    """ Checks if a user has certain permission over an object

    :param user: django auth user object
    :param operation:  string, rbac operation
    :param object_name: string, the name of the subject
    :return Boolean, true if the user has permission, False if not
    """
    user_role = UserRole.objects.filter(
        user=user, role__status='active').exclude(status=False)
    operation_obj = get_object_or_404(Operation, operation=operation)
    for u_role in user_role:
        permission = PermissonAssignment.objects.filter(
            object__object=object_name,
            role=u_role.role, operation=operation_obj)
        if permission:
            return True
    return False


def is_user_role(user, role_str):
    """ Checks if a user has certain role

    :param user: django auth user object
    :type user: User
    :param role_str:  string, role name
    :type role_str: basestring
    :return Boolean, true if the user has that role, False if not
    :rtype: bool
    """
    user_role = UserRole.objects.\
        filter(user=user, role__status='active', role__role=role_str).\
        exclude(status=False)

    if user_role:
        return True
    else:
        return False


def get_user_roles(user):
    """ Get the user roles

    :param user: the user
    :return: an array of role names
    """
    roles = UserRole.objects.filter(
        user=user
    ).order_by('role__importance').values_list('role__role', flat=True)
    return roles
