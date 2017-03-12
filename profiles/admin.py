import datetime
from django.contrib import admin
from profiles.models import Profile, Address


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['auth_user']
    list_display = ['auth_user', 'dream_worker', 'phone']


class AddressAdmin(admin.ModelAdmin):
    search_fields = ['address']
    list_display = ['profile', 'address', 'city']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
