# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rbac.models import Role, UserRole

# from users.models import User
from .models import Profile


def save_user_as_client(first_name, last_name, email, password):
    """
    Records a Django User with a Client role.
    :param first_name: Nombre del usuario.
    :param last_name: Apellido del usuario.
    :param email: Correo electrónico del usuario.
    :param password: Contraseña del usuario.
    """

    user_created = False
    user, flag = User.objects.get_or_create(
        email=email,
        username=email
    )
    user.first_name = first_name
    user.last_name = last_name
    user.set_password(password)
    user.save()
    if flag:
        user.save()
        user_created = True
        role, created = Role.objects.get_or_create(role='Client')

        user_role = UserRole()
        user_role.user = user
        user_role.role = role
        user_role.save()

        profile = Profile()
        profile.email = email
        profile.auth_user = user
        profile.save()

    return user_created
