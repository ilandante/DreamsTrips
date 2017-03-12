# -*- coding: utf-8 -*-
import csv

from django.core.exceptions import MultipleObjectsReturned

from location.models import Country, AirPort, City


def fix_cities():
    cities = City.objects.all()
    for city in cities:
        city.country = city.state.country
        city.save()
        print city
    print 'done'


def parse_airport(path):
    data = csv.reader(open(path, "U"))
    # Read the column names from the first line of the file
    fields = data.next()
    for row in data:
        # Zip together the field names and values
        items = zip(fields, row)
        item = {}
        # Add the value to our dictionary
        for (name, value) in items:
            item[name.strip()] = value.strip()

        # keys: id,name,city,country,IATA,ICAO,latitude,longitude,altitude,timezone,dst,tz
        country, created_c = Country.objects.get_or_create(
            name=item['country']
        )
        print 'country', created_c
        try:
            city, created_s = City.objects.get_or_create(
                country=country,
                name=item['city']
            )
            print 'city', created_s
        except MultipleObjectsReturned:
            city = City.objects.filter(country=country,
                                       name=item['city']
                                       ).first()
            print city

        airport, created_a = AirPort.objects.get_or_create(
            name=item['name'],
            city=city,
            identifier=item['IATA']
        )
        print 'airport', created_a