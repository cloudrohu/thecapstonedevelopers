from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from apps.business_utility.models import BusinessDocumentType
from apps.business_utility.resources import BusinessDocumentTypeResource


@admin.register(BusinessDocumentType)
class BusinessDocumentTypeAdmin(ImportExportModelAdmin):

    resource_class = BusinessDocumentTypeResource

    save_on_top = True

    save_as = True

    list_per_page = 50

    search_fields = (
        "name",
        "code",
        "slug",
    )

    list_display = (
        "name",
        "code",
        "display_order",
        "is_active",
    )

    list_display_links = (
        "name",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    prepopulated_fields = {
        "slug": (
            "name",
        ),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "display_order",
        "name",
    )

    fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "code",
                    "slug",
                    "description",
                )
            },
        ),

        (
            "Settings",
            {
                "fields": (
                    "display_order",
                    "is_active",
                )
            },
        ),

        (
            "System Information",
            {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),

    )