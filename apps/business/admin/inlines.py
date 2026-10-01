from django.contrib import admin

from apps.business.models import (
    BusinessGallery,
    BusinessTiming,
    BusinessHoliday,
    BusinessDocument,
    BusinessSocialLink,
    BusinessAttributeValue,
)

class BusinessGalleryInline(admin.TabularInline):

    model = BusinessGallery

    extra = 1

    fields = (
        "gallery_type",
        "title",
        "image",
        "display_order",
        "is_featured",
        "is_active",
    )

    ordering = (
        "display_order",
    )

class BusinessTimingInline(admin.TabularInline):

    model = BusinessTiming

    extra = 0

    fields = (
        "day",
        "opening_time",
        "closing_time",
        "is_closed",
        "is_24_hours",
    )

class BusinessHolidayInline(admin.TabularInline):

    model = BusinessHoliday

    extra = 0

    fields = (
        "title",
        "holiday_date",
        "description",
    )

class BusinessSocialLinkInline(admin.TabularInline):

    model = BusinessSocialLink

    extra = 0

    fields = (
        "platform",
        "url",
        "username",
        "is_primary",
    )

class BusinessDocumentInline(admin.TabularInline):

    model = BusinessDocument

    extra = 0

    fields = (
        "document_type",
        "document_number",
        "document",
        "verification_status",
    )

class BusinessAttributeValueInline(admin.TabularInline):

    model = BusinessAttributeValue

    extra = 0

    fields = (
        "attribute",
        "value",
    )