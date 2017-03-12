# # -*- coding: utf-8 -*-
#
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.utils.translation import ugettext_lazy as _
#
# from experiences.models import Review
# from finances.models import Card
# from users.models import Profile, Address, Country
#
#


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User

        fields = [
            'first_name', 'last_name',
            'email',
            'password1', 'password2',
        ]

        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email address'),
            'password1': _('Password'),
            'password2': _('Password confirmation'),
        }

    email = forms.EmailField(required=True)
#
#
# class UserLoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['email', 'password', ]
#         labels = {'email': _('Email address'), 'password': _('Password'), }
#     email = forms.EmailField(required=True)
#
#
# class ProfileUpdateForm(forms.ModelForm):
#     first_name = forms.CharField(required=True, max_length=64)
#     last_name = forms.CharField(required=False, max_length=64)
#
#     class Meta:
#         model = Profile
#
#         fields = [
#             'email', 'phone', 'birthdate', 'bio', 'languages', 'gender',
#             'picture'
#         ]
#
#         labels = {
#             'email': _('Email address')
#         }
#
#
# class AddressUpdateForm(forms.ModelForm):
#     country = forms.ModelChoiceField(required=False,
#                                      queryset=Country.objects.all(),
#                                      label="País")
#     latitude = forms.CharField(required=True)
#     longitude = forms.CharField(required=True)
#
#     class Meta:
#         model = Address
#         fields = [
#             'city', 'address', 'zipcode', 'profile', 'latitude', 'longitude'
#         ]
#
#
# # class CardUpdateForm(forms.ModelForm):
# #     profile = forms.ModelChoiceField(required=False,
# #                                      queryset=Profile.objects.all()
# #                                      )
# #
# #     class Meta:
# #         model = Card
# #
# #         fields = [
# #             'cardholder', 'pan', 'valid_through_month', 'valid_through_year',
# #             'ccv', 'profile'
# #         ]
#
