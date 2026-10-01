from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from apps.business.models import BusinessSocialLink
from apps.business.resources import BusinessSocialLinkResource


@admin.register(BusinessSocialLink)
class BusinessSocialLinkAdmin(ImportExportModelAdmin):

    resource_class = BusinessSocialLinkResource

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
        "platform",
        "username",
        "url",
        "is_primary",
        "is_active",
    )

    list_display_links = (
        "business",
    )

    search_fields = (
        "business__name",
        "username",
        "url",
    )

    list_filter = (
        "platform",
        "is_primary",
        "is_active",
    )

    ordering = (
        "business",
        "platform",
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
            "Social Information",
            {
                "fields": (
                    "platform",
                    "username",
                    "url",
                    "is_primary",
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
        "make_primary",
        "remove_primary",
        "make_active",
        "make_inactive",
    )

    @admin.action(description="⭐ Mark as Primary")
    def make_primary(self, request, queryset):

        count = queryset.update(
            is_primary=True,
        )

        self.message_user(
            request,
            f"{count} social link(s) marked as primary.",
        )

    @admin.action(description="Remove Primary")
    def remove_primary(self, request, queryset):

        count = queryset.update(
            is_primary=False,
        )

        self.message_user(
            request,
            f"{count} social link(s) removed from primary.",
        )

    @admin.action(description="✅ Activate")
    def make_active(self, request, queryset):

        count = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            f"{count} social link(s) activated.",
        )

    @admin.action(description="❌ Deactivate")
    def make_inactive(self, request, queryset):

        count = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            f"{count} social link(s) deactivated.",
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