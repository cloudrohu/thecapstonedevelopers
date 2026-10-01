from django.contrib import admin

from apps.utility.models import (
    Language,
    Currency,
    CountryCode,
    Religion,
    Education,
    MaritalStatus,
)

from .base import MasterAdmin


@admin.register(Language)
class LanguageAdmin(MasterAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(MasterAdmin):
    pass


@admin.register(CountryCode)
class CountryCodeAdmin(MasterAdmin):

    list_display = (
        "name",
        "dial_code",
        "is_active",
    )


@admin.register(Religion)
class ReligionAdmin(MasterAdmin):
    pass


@admin.register(Education)
class EducationAdmin(MasterAdmin):
    pass


@admin.register(MaritalStatus)
class MaritalStatusAdmin(MasterAdmin):
    pass