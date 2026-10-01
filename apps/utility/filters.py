from django.contrib.admin import SimpleListFilter

from apps.utility.models import Location, LocationType


class StateFilter(SimpleListFilter):
    title = "State"
    parameter_name = "state"

    def lookups(self, request, model_admin):
        return [
            (obj.id, obj.name)
            for obj in Location.objects.filter(
                location_type=LocationType.STATE,
                is_active=True
            ).order_by("name")
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent_id=self.value())
        return queryset


class DistrictCityFilter(SimpleListFilter):
    title = "District / City"
    parameter_name = "district_city"

    def lookups(self, request, model_admin):
        return [
            (obj.id, obj.name)
            for obj in Location.objects.filter(
                location_type=LocationType.DISTRICT_CITY,
                is_active=True
            ).order_by("name")
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent_id=self.value())
        return queryset


class LocalityFilter(SimpleListFilter):
    title = "Locality / Area"
    parameter_name = "locality"

    def lookups(self, request, model_admin):
        return [
            (obj.id, obj.name)
            for obj in Location.objects.filter(
                location_type=LocationType.LOCALITY_AREA,
                is_active=True
            ).order_by("name")
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent_id=self.value())
        return queryset