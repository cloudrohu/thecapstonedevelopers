from django.contrib import admin

from apps.enquiries.models import EnquirySource


@admin.register(EnquirySource)
class EnquirySourceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sort_order",
        "is_active",
    )

    list_filter = (
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