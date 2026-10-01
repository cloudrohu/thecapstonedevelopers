from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin

from apps.business.models import (
    BusinessFollowUp,
    FollowUpStatus,
    FollowUpMode,
)
from apps.business.resources import (
    BusinessFollowUpResource,
)


@admin.register(BusinessFollowUp)
class BusinessFollowUpAdmin(ImportExportModelAdmin):

    resource_class = BusinessFollowUpResource

    save_on_top = True

    save_as = True

    list_per_page = 50

    list_max_show_all = 500

    date_hierarchy = "followup_date"

    empty_value_display = "-"

    autocomplete_fields = (
        "enquiry",
        "assigned_to",
    )

    list_select_related = (
        "enquiry",
        "assigned_to",
    )

    list_display = (
        "enquiry",
        "followup_date",
        "followup_time",
        "mode_badge",
        "status_badge",
        "assigned_to",
        "next_followup_date",
    )

    list_display_links = (
        "enquiry",
    )

    search_fields = (
        "enquiry__customer_name",
        "enquiry__business__name",
        "remarks",
    )

    list_filter = (
        "mode",
        "status",
        "assigned_to",
        "followup_date",
    )

    ordering = (
        "-followup_date",
        "-followup_time",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Enquiry",
            {
                "fields": (
                    "enquiry",
                )
            },
        ),

        (
            "Follow Up",
            {
                "fields": (
                    (
                        "followup_date",
                        "followup_time",
                    ),
                    "mode",
                    "status",
                    "remarks",
                )
            },
        ),

        (
            "Next Follow Up",
            {
                "fields": (
                    "next_followup_date",
                    "assigned_to",
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

    @admin.display(description="Mode")
    def mode_badge(self, obj):

        colors = {
            FollowUpMode.CALL: "#0d6efd",
            FollowUpMode.WHATSAPP: "#25D366",
            FollowUpMode.EMAIL: "#6610f2",
            FollowUpMode.SMS: "#20c997",
            FollowUpMode.VISIT: "#fd7e14",
            FollowUpMode.MEETING: "#198754",
            FollowUpMode.OTHER: "#6c757d",
        }

        return format_html(
            '<span style="background:{};color:white;'
            'padding:4px 10px;border-radius:15px;">'
            '{}'
            '</span>',
            colors.get(obj.mode, "#6c757d"),
            obj.get_mode_display(),
        )

    @admin.display(description="Status")
    def status_badge(self, obj):

        colors = {
            FollowUpStatus.PENDING: "#ffc107",
            FollowUpStatus.COMPLETED: "#198754",
            FollowUpStatus.CANCELLED: "#dc3545",
        }

        return format_html(
            '<span style="background:{};color:white;'
            'padding:4px 10px;border-radius:15px;">'
            '{}'
            '</span>',
            colors.get(obj.status, "#6c757d"),
            obj.get_status_display(),
        )

    actions = (
        "mark_completed",
        "mark_pending",
        "mark_cancelled",
    )

    @admin.action(description="✅ Mark as Completed")
    def mark_completed(self, request, queryset):

        count = queryset.update(
            status=FollowUpStatus.COMPLETED,
        )

        self.message_user(
            request,
            f"{count} follow-up(s) marked as completed.",
        )

    @admin.action(description="⏳ Mark as Pending")
    def mark_pending(self, request, queryset):

        count = queryset.update(
            status=FollowUpStatus.PENDING,
        )

        self.message_user(
            request,
            f"{count} follow-up(s) marked as pending.",
        )

    @admin.action(description="❌ Mark as Cancelled")
    def mark_cancelled(self, request, queryset):

        count = queryset.update(
            status=FollowUpStatus.CANCELLED,
        )

        self.message_user(
            request,
            f"{count} follow-up(s) marked as cancelled.",
        )

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "enquiry",
                "assigned_to",
                "enquiry__business",
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