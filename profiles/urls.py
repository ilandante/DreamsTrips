# # -*- coding: utf-8 -*-
#
# from django.conf.urls import url
#
# from .views import UserRegisterView, user_login, update_profile_view, \
#     profile_update, logout_page, change_password, ViewProfile, save_address, \
#     get_address, add_review
#
# urlpatterns = [
#     url(r'^$', user_login, name='user_login'),
#     url(r'^logout$', logout_page, name='logout'),
#     url(r'^register/$', UserRegisterView.as_view(), name='user_register'),
#     url(r'^update/$', update_profile_view, name='update_profile'),
#     url(r'^update_user/(?P<user_pk>\d+)/$', profile_update,
#         name='update_profile_forms'),
#     url(r'^change_password/$', change_password, name="change_password"),
#     url(r'^profile/(?P<profile_pk>\d+)/$',
#         ViewProfile.as_view(), name='single_profile'),
#     url(r'^add_review/(?P<pk>\d+)/$',
#         add_review, name='add_review'),
#
#     url(r'^save_address/(?P<address_pk>\d+)/$', save_address,
#         name='save_address'),
#     url(r'^get_address/(?P<address_pk>\d+)/$', get_address,
#         name='get_address')
# ]
