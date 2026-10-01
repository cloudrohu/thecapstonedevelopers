from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin

from apps.business.models import BusinessGallery
from apps.business.resources import BusinessGalleryResource


@admin.register(BusinessGallery)
class BusinessGalleryAdmin(ImportExportModelAdmin):

    resource_class = BusinessGalleryResource

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
        "image_preview",
        "business",
        "title",
        "gallery_type",
        "display_order",
        "is_featured",
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
        "gallery_type",
        "is_featured",
        "is_active",
    )

    ordering = (
        "business",
        "display_order",
    )

    readonly_fields = (
        "image_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Gallery Information",
            {
                "fields": (
                    "business",
                    "gallery_type",
                    "title",
                    "description",
                    "display_order",
                )
            },
        ),

        (
            "Media",
            {
                "fields": (
                    "image",
                    "image_preview",
                )
            },
        ),

        (
            "Status",
            {
                "fields": (
                    "is_featured",
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

    @admin.display(description="Image")
    def image_preview(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" '
                'style="width:70px;height:70px;'
                'object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )

        return "-"

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "business",
            )
        )

    actions = (
        "make_featured",
        "remove_featured",
        "make_active",
        "make_inactive",
    )

    @admin.action(description="⭐ Mark as Featured")
    def make_featured(self, request, queryset):

        count = queryset.update(
            is_featured=True,
        )

        self.message_user(
            request,
            f"{count} gallery image(s) marked as featured.",
        )

    @admin.action(description="Remove Featured")
    def remove_featured(self, request, queryset):

        count = queryset.update(
            is_featured=False,
        )

        self.message_user(
            request,
            f"{count} gallery image(s) removed from featured.",
        )

    @admin.action(description="✅ Activate")
    def make_active(self, request, queryset):

        count = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            f"{count} gallery image(s) activated.",
        )

    @admin.action(description="❌ Deactivate")
    def make_inactive(self, request, queryset):

        count = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            f"{count} gallery image(s) deactivated.",
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