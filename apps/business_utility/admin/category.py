from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from apps.business_utility.models import BusinessCategory
from apps.business_utility.resources import BusinessCategoryResource


@admin.register(BusinessCategory)
class BusinessCategoryAdmin(
    DraggableMPTTAdmin,
    ImportExportModelAdmin,
):
    resource_class = BusinessCategoryResource

    mptt_indent_field = "name"

    prepopulated_fields = {
        "slug": ("name",),
    }

    search_fields = (
        "name",
        "code",
        "slug",
    )

    list_display = (
        "tree_actions",
        "indented_title",
        "parent",
        "display_order",
        "is_featured",
        "is_active",
    )

    list_display_links = (
        "indented_title",
    )

    list_editable = (
        "display_order",
        "is_featured",
        "is_active",
    )

    list_filter = (
        "is_featured",
        "is_active",
    )

    ordering = (
        "tree_id",
        "lft",
    )

    readonly_fields = (
        "icon_preview",
        "banner_preview",
        "created_at",
        "updated_at",
    )

    save_on_top = True

    list_per_page = 50

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
            "Hierarchy",
            {
                "fields": (
                    "parent",
                    "display_order",
                )
            },
        ),

        (
            "Media",
            {
                "fields": (
                    "icon",
                    "icon_preview",
                    "banner",
                    "banner_preview",
                )
            },
        ),

        (
            "Appearance",
            {
                "fields": (
                    "icon_class",
                    "color",
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
            "System",
            {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(description="Icon")
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:6px;">',
                obj.icon.url,
            )
        return "-"

    @admin.display(description="Banner")
    def banner_preview(self, obj):
        if obj.banner:
            return format_html(
                '<img src="{}" width="180" style="border-radius:6px;">',
                obj.banner.url,
            )
        return "-"

    actions = (
        "make_active",
        "make_inactive",
        "make_featured",
        "remove_featured",
    )

    @admin.action(description="Mark selected categories as Active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Mark selected categories as Inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Mark selected categories as Featured")
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Remove Featured")
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)