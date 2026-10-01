from django.contrib import admin

from apps.enquiries.models import Response
from .followup import FollowupInline
from .meeting import MeetingInline
from .response_note import ResponseNoteInline
from .response_document import ResponseDocumentInline

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    inlines = [
        FollowupInline,
        MeetingInline,
        ResponseNoteInline,
        ResponseDocumentInline,
    ]
    list_display = (
        "response_no",
        "enquiry",
        "status",
        "priority",
        "assigned_to",
        "next_followup_at",
        "is_converted",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "is_converted",
        "assigned_to",
        "created_at",
    )

    search_fields = (
        "response_no",
        "enquiry__enquiry_no",
        "enquiry__customer__name",
        "enquiry__customer__mobile",
        "enquiry__customer__email",
    )

    autocomplete_fields = (
        "enquiry",
        "status",
        "assigned_to",
    )

    readonly_fields = (
        "response_no",
        "first_response_at",
        "last_activity_at",
        "converted_at",
        "closed_at",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    list_select_related = (
        "enquiry",
        "status",
        "assigned_to",
    )

    fieldsets = (
        (
            "Response Information",
            {
                "fields": (
                    "response_no",
                    "enquiry",
                    "status",
                    "assigned_to",
                    "priority",
                )
            },
        ),
        (
            "Timeline",
            {
                "fields": (
                    "first_response_at",
                    "last_activity_at",
                    "next_followup_at",
                )
            },
        ),
        (
            "Conversion",
            {
                "fields": (
                    "is_converted",
                    "converted_at",
                    "closed_at",
                )
            },
        ),
        (
            "Remarks",
            {
                "fields": (
                    "remarks",
                )
            },
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )