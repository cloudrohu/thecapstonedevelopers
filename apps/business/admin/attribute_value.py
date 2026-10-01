from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from apps.business.models import BusinessAttributeValue
from apps.business.resources import BusinessAttributeValueResource


@admin.register(BusinessAttributeValue)
class BusinessAttributeValueAdmin(ImportExportModelAdmin):

    resource_class = BusinessAttributeValueResource

    save_on_top = True

    save_as = True

    list_per_page = 50

    list_max_show_all = 500

    date_hierarchy = "created_at"

    empty_value_display = "-"

    autocomplete_fields = (
        "business",
        "attribute",
    )

    list_select_related = (
        "business",
        "attribute",
    )

    list_display = (
        "business",
        "attribute",
        "value",
        "is_active",
    )

    list_display_links = (
        "attribute",
    )

    search_fields = (
        "business__name",
        "attribute__name",
        "value",
    )

    list_filter = (
        "attribute",
        "is_active",
    )

    ordering = (
        "business",
        "attribute",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Business",
            {
                "fields": (
                    "business",
                    "attribute",
                )
            },
        ),

        (
            "Attribute Value",
            {
                "fields": (
                    "value",
                )
            },
        ),

        (
            "Status",
            {
                "fields": (
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

    actions = (
        "make_active",
        "make_inactive",
    )

    @admin.action(description="✅ Activate Selected Values")
    def make_active(self, request, queryset):

        count = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            f"{count} attribute value(s) activated.",
        )

    @admin.action(description="❌ Deactivate Selected Values")
    def make_inactive(self, request, queryset):

        count = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            f"{count} attribute value(s) deactivated.",
        )

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "business",
                "attribute",
            )
        )

    def save_model(self, request, obj, form, change):

        if not change:
            obj.created_by = request.user

        obj.updated_by = request.user

        super().save_model(
            request,
            obj,
            form,
            change,
        )