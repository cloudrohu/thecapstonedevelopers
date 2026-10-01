from django.contrib import admin

from apps.utility.models import (
    Location,
    LocationType,
)


class CityFilter(admin.SimpleListFilter):

    title = "City"
    parameter_name = "city"

    def lookups(self, request, model_admin):

        cities = Location.objects.filter(
            location_type=LocationType.DISTRICT_CITY,
            is_active=True,
        )

        return [
            (city.id, city.name)
            for city in cities
        ]

    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(city_id=self.value())

        return queryset


class LocalityFilter(admin.SimpleListFilter):

    title = "Locality"
    parameter_name = "locality"

    def lookups(self, request, model_admin):

        data = Location.objects.filter(
            location_type=LocationType.LOCALITY_AREA,
            is_active=True,
        )

        return [
            (obj.id, obj.name)
            for obj in data
        ]

    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(locality_id=self.value())

        return queryset


class AreaFilter(admin.SimpleListFilter):

    title = "Area"
    parameter_name = "area"

    def lookups(self, request, model_admin):

        data = Location.objects.filter(
            location_type=LocationType.SUBLOCALITY_AREA,
            is_active=True,
        )

        return [
            (obj.id, obj.name)
            for obj in data
        ]

    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(area_id=self.value())

        return queryset


class VerifiedFilter(admin.SimpleListFilter):

    title = "Verified"
    parameter_name = "verified"

    def lookups(self, request, model_admin):
        return (
            ("1", "Verified"),
            ("0", "Not Verified"),
        )

    def queryset(self, request, queryset):

        if self.value() == "1":
            return queryset.filter(is_verified=True)

        if self.value() == "0":
            return queryset.filter(is_verified=False)

        return queryset