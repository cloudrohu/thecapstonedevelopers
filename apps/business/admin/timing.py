from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from apps.business.models import BusinessTiming
from apps.business.resources import BusinessTimingResource


@admin.register(BusinessTiming)
class BusinessTimingAdmin(ImportExportModelAdmin):

    resource_class = BusinessTimingResource

    save_on_top = True

    save_as = True

    list_per_page = 50

    list_max_show_all = 500

    date_hierarchy = "created_at"

    empty_value_display = "-"

    autocomplete_fields = (
        "business",
    )

    list_select_related = (
        "business",
    )

    list_display = (
        "business",
        "day",
        "opening_time",
        "closing_time",
        "is_closed",
        "is_24_hours",
        "is_active",
    )

    list_display_links = (
        "business",
    )

    search_fields = (
        "business__name",
    )

    list_filter = (
        "day",
        "is_closed",
        "is_24_hours",
        "is_active",
    )

    ordering = (
        "business",
        "day",
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
                )
            },
        ),

        (
            "Timing",
            {
                "fields": (
                    "day",
                    (
                        "opening_time",
                        "closing_time",
                    ),
                    "is_closed",
                    "is_24_hours",
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
        "mark_closed",
        "mark_open_24_hours",
    )

    @admin.action(description="✅ Activate Selected Timings")
    def make_active(self, request, queryset):

        count = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            f"{count} timing(s) activated.",
        )

    @admin.action(description="❌ Deactivate Selected Timings")
    def make_inactive(self, request, queryset):

        count = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            f"{count} timing(s) deactivated.",
        )

    @admin.action(description="🚫 Mark as Closed")
    def mark_closed(self, request, queryset):

        count = queryset.update(
            is_closed=True,
            is_24_hours=False,
        )

        self.message_user(
            request,
            f"{count} timing(s) marked as closed.",
        )

    @admin.action(description="🕒 Mark as 24 Hours Open")
    def mark_open_24_hours(self, request, queryset):

        count = queryset.update(
            is_24_hours=True,
            is_closed=False,
        )

        self.message_user(
            request,
            f"{count} timing(s) marked as 24 hours.",
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