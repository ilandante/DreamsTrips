# -*- coding: utf-8 -*-
__author__ = 'rafa'
from _socket import error
import random
import string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.conf import settings




def is_valid_email(email):
    """ check if a string is a valid email address
    django dependant

    @param email: - the string to evaluate
    @return: boolean, True if valid, False if not

    >>> is_valid_email("hector@wime.com.mx")
    True
    >>> is_valid_email("foobar")
    False
    """
    try:
        from django.core.validators import email_re
        return True if email_re.match(email) else False
    except ImportError:
        from django.core.validators import validate_email
        return True if validate_email(email) else False


def reset_pass(email):
    new_pass = random_string_generator()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        pass
    else:
        user.set_password(new_pass)
        domain = settings.DOMAIN
        url_sys = 'http://'+domain
        subject, from_email, to = 'Reseteo de contraseña', \
                                  'noresponse@{0}'.format(domain), email
        text_content = 'Su contraseña ha sido restablecida, puede ingresar ' \
                       'al sistema ({0}) con su nombre de usuario y ' \
                       'la contraseña: {1} \n Una vez dentro del sistema, ' \
                       'podrá cambiar su contraseña por la que usted desee'\
            .format(url_sys, new_pass)
        html_content = '<h1>Su contraseña ha sido restablecida</h1>' \
                       '<p>Puede ingresar al <a href="{0}">sistema escolar ' \
                       'con su nombre de usuario y contraseña:</p>' \
                       '<p style="text-align:center;">{1}</p>' \
                       '<p>Una vez dentro del sistema, podrá cambiar su ' \
                       'contraseña por la que usted desee</p>'\
            .format(url_sys, new_pass)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except error:
            print "Is the email server online?"
    return


def random_string_generator(size=6,
                            chars=string.ascii_uppercase + string.digits):
    """Random String Generator

    @param size: longitud de la cadena (default 6)
    @param chars: caracteres de entre los que generara la cadena
                  (default [A-Z0-9])
    @return: generated random string
    >>> random_string_generator()
    'G5G74W'
    >>> random_string_generator(3, "6793YUIO")
    'Y3U'

    """
    return ''.join(random.choice(chars) for x in range(size))

