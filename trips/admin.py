import datetime
from django.contrib import admin
from .models import Trip, Itinerary, TripGallery, GalleryImage


class TripsAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'seats_available', 'init_date', 'end_date']


class ItineraryAdmin(admin.ModelAdmin):
    search_fields = ['trip']
    list_display = ['name', 'description', 'trip']


class TripGalleryAdmin(admin.ModelAdmin):
    search_fields = ['trip']
    list_display = ['trip']


class GalleryImageAdmin(admin.ModelAdmin):
    search_fields = ['gallery', 'pk']
    list_display = ['photograph', 'pk', 'gallery']


admin.site.register(Trip, TripsAdmin)
admin.site.register(Itinerary, ItineraryAdmin)
admin.site.register(TripGallery, TripGalleryAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)

