from django.contrib import admin

from apps.enquiries.models import Meeting


class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 0

    fields = (
        "meeting_no",
        "meeting_type",
        "status",
        "meeting_date",
        "assigned_to",
    )

    readonly_fields = (
        "meeting_no",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "assigned_to",
    )

    ordering = (
        "-meeting_date",
    )


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):

    list_display = (
        "meeting_no",
        "response",
        "meeting_type",
        "status",
        "meeting_date",
        "assigned_to",
    )

    list_filter = (
        "status",
        "meeting_type",
    )

    search_fields = (
        "meeting_no",
        "response__response_no",
    )

    autocomplete_fields = (
        "response",
        "assigned_to",
    )