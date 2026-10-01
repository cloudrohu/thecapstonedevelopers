from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin


class MasterAdmin(ImportExportModelAdmin):
    list_display = ("name", "code", "is_active")

    search_fields = ("name", "code", "slug")

    list_filter = ("is_active",)

    list_editable = ("is_active",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = ("name",)

    save_on_top = True

    list_per_page = 50


class ColorMasterAdmin(MasterAdmin):

    @admin.display(description="Color")
    def color_preview(self, obj):
        return format_html(
            '<span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:{};"></span>',
            obj.color,
        )