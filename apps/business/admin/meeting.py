from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin

from apps.business.models import (
    BusinessMeeting,
    MeetingStatus,
    MeetingType,
)
from apps.business.resources import (
    BusinessMeetingResource,
)


@admin.register(BusinessMeeting)
class BusinessMeetingAdmin(ImportExportModelAdmin):

    resource_class = BusinessMeetingResource

    save_on_top = True

    save_as = True

    list_per_page = 50

    list_max_show_all = 500

    date_hierarchy = "meeting_date"

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
        "meeting_date",
        "meeting_time",
        "meeting_type_badge",
        "status_badge",
        "assigned_to",
    )

    list_display_links = (
        "enquiry",
    )

    search_fields = (
        "enquiry__customer_name",
        "enquiry__business__name",
        "meeting_location",
        "agenda",
        "outcome",
    )

    list_filter = (
        "meeting_type",
        "status",
        "assigned_to",
        "meeting_date",
    )

    ordering = (
        "-meeting_date",
        "-meeting_time",
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
            "Meeting Information",
            {
                "fields": (
                    "meeting_type",
                    (
                        "meeting_date",
                        "meeting_time",
                    ),
                    "meeting_location",
                )
            },
        ),

        (
            "Discussion",
            {
                "fields": (
                    "agenda",
                    "outcome",
                    "next_action",
                )
            },
        ),

        (
            "Assignment",
            {
                "fields": (
                    "assigned_to",
                    "status",
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

    @admin.display(description="Meeting Type")
    def meeting_type_badge(self, obj):

        colors = {
            MeetingType.OFFICE: "#0d6efd",
            MeetingType.SITE_VISIT: "#fd7e14",
            MeetingType.ONLINE: "#198754",
            MeetingType.PHONE: "#6610f2",
            MeetingType.OTHER: "#6c757d",
        }

        return format_html(
            '<span style="background:{};'
            'color:white;'
            'padding:4px 10px;'
            'border-radius:15px;">'
            '{}'
            '</span>',
            colors.get(obj.meeting_type, "#6c757d"),
            obj.get_meeting_type_display(),
        )

    @admin.display(description="Status")
    def status_badge(self, obj):

        colors = {
            MeetingStatus.SCHEDULED: "#0d6efd",
            MeetingStatus.COMPLETED: "#198754",
            MeetingStatus.CANCELLED: "#dc3545",
            MeetingStatus.RESCHEDULED: "#fd7e14",
        }

        return format_html(
            '<span style="background:{};'
            'color:white;'
            'padding:4px 10px;'
            'border-radius:15px;">'
            '{}'
            '</span>',
            colors.get(obj.status, "#6c757d"),
            obj.get_status_display(),
        )

    actions = (
        "mark_completed",
        "mark_cancelled",
        "mark_rescheduled",
        "mark_scheduled",
    )

    @admin.action(description="✅ Mark as Completed")
    def mark_completed(self, request, queryset):

        count = queryset.update(
            status=MeetingStatus.COMPLETED,
        )

        self.message_user(
            request,
            f"{count} meeting(s) marked as completed.",
        )

    @admin.action(description="❌ Mark as Cancelled")
    def mark_cancelled(self, request, queryset):

        count = queryset.update(
            status=MeetingStatus.CANCELLED,
        )

        self.message_user(
            request,
            f"{count} meeting(s) marked as cancelled.",
        )

    @admin.action(description="🔄 Mark as Rescheduled")
    def mark_rescheduled(self, request, queryset):

        count = queryset.update(
            status=MeetingStatus.RESCHEDULED,
        )

        self.message_user(
            request,
            f"{count} meeting(s) marked as rescheduled.",
        )

    @admin.action(description="📅 Mark as Scheduled")
    def mark_scheduled(self, request, queryset):

        count = queryset.update(
            status=MeetingStatus.SCHEDULED,
        )

        self.message_user(
            request,
            f"{count} meeting(s) marked as scheduled.",
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