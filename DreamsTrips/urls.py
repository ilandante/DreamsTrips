"""DreamsTrips URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import django.views.static
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from DreamsTrips.views import home_view, mission_view, \
    DreamWorkersListView, send_contact_message
from trips import urls as trips_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Project apps
    url(r'^$', home_view, name='home'),
    url(r'^mission/$', mission_view, name='mission'),
    url(r'^team/$', DreamWorkersListView.as_view(), name='team'),
    url(r'^trips/', include(trips_urls)),
    # url(r'^profile/', include('profiles.urls')),
    url(r'^send_contact_message/', send_contact_message, name="send_contact_message"),

    url(r'^static/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

]
