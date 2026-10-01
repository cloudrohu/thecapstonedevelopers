from django.contrib import admin

from apps.enquiries.models import Followup


class FollowupInline(admin.TabularInline):
    model = Followup
    extra = 0

    fields = (
        "followup_no",
        "followup_type",
        "status",
        "followup_date",
        "assigned_to",
    )

    readonly_fields = (
        "followup_no",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "assigned_to",
    )

    ordering = (
        "-followup_date",
    )


@admin.register(Followup)
class FollowupAdmin(admin.ModelAdmin):

    list_display = (
        "followup_no",
        "response",
        "followup_type",
        "status",
        "followup_date",
        "assigned_to",
    )

    list_filter = (
        "status",
        "followup_type",
        "assigned_to",
    )

    search_fields = (
        "followup_no",
        "response__response_no",
    )

    autocomplete_fields = (
        "response",
        "assigned_to",
    )