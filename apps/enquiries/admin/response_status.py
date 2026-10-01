from django.contrib import admin

from apps.enquiries.models import ResponseStatus


@admin.register(ResponseStatus)
class ResponseStatusAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_default",
        "is_closed",
        "sort_order",
        "is_active",
    )

    list_filter = (
        "is_default",
        "is_closed",
        "is_active",
    )

    search_fields = (
        "name",
        "slug",
    )

    ordering = (
        "sort_order",
        "name",
    )