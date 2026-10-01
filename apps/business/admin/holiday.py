from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from apps.business.models import BusinessHoliday
from apps.business.resources import BusinessHolidayResource


@admin.register(BusinessHoliday)
class BusinessHolidayAdmin(ImportExportModelAdmin):

    resource_class = BusinessHolidayResource

    save_on_top = True

    save_as = True

    list_per_page = 50

    list_max_show_all = 500

    date_hierarchy = "holiday_date"

    empty_value_display = "-"

    autocomplete_fields = (
        "business",
    )

    list_select_related = (
        "business",
    )

    list_display = (
        "business",
        "title",
        "holiday_date",
        "is_active",
    )

    list_display_links = (
        "title",
    )

    search_fields = (
        "title",
        "business__name",
    )

    list_filter = (
        "holiday_date",
        "is_active",
    )

    ordering = (
        "-holiday_date",
        "business",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Holiday Information",
            {
                "fields": (
                    "business",
                    "title",
                    "holiday_date",
                    "description",
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

    @admin.action(description="✅ Activate Selected Holidays")
    def make_active(self, request, queryset):

        count = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            f"{count} holiday(s) activated.",
        )

    @admin.action(description="❌ Deactivate Selected Holidays")
    def make_inactive(self, request, queryset):

        count = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            f"{count} holiday(s) deactivated.",
        )

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "business",
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