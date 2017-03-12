# -*- coding: utf-8 -*-

from rbac.models import Role


def populate_roles():
    roles_pupulation = [
        {'role': 'Administrador'},
        {'role': 'Guest'},
        {'role': 'Host'},
    ]

    for role in roles_pupulation:
        Role.objects.update_or_create(role=role['role'])
