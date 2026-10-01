from django.contrib import admin
from django.utils.html import format_html

from .models import ImportProject


@admin.register(ImportProject)
class ImportProjectAdmin(admin.ModelAdmin):

    list_display = (
        "website",
        "url_short",
        "status_badge",
        "project",
        "created_at",
    )

    readonly_fields = (
        "status",
        "project",
        "started_at",
        "completed_at",
        "log",
        "error",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "url",
        "project__project_name",
    )

    list_filter = (
        "website",
        "status",
    )

    ordering = (
        "-created_at",
    )

    actions = (
        "start_import",
    )

    def url_short(self, obj):
        if len(obj.url) > 70:
            return obj.url[:70] + "..."
        return obj.url

    url_short.short_description = "URL"

    def status_badge(self, obj):

        colors = {
            "Pending": "#f39c12",
            "Running": "#3498db",
            "Completed": "#27ae60",
            "Failed": "#e74c3c",
        }

        color = colors.get(obj.status, "#999")

        return format_html(
            '<span style="background:{};color:white;padding:5px 10px;border-radius:20px;">{}</span>',
            color,
            obj.status,
        )

    status_badge.short_description = "Status"

    @admin.action(description="Start Import")
    def start_import(self, request, queryset):

        from .services import ImportService

        for item in queryset:
            ImportService(item).run()