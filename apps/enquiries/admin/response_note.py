from django.contrib import admin

from apps.enquiries.models import ResponseNote


class ResponseNoteInline(admin.TabularInline):
    model = ResponseNote
    extra = 0

    fields = (
        "note",
        "is_private",
        "created_by",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "created_by",
    )


@admin.register(ResponseNote)
class ResponseNoteAdmin(admin.ModelAdmin):

    list_display = (
        "response",
        "created_by",
        "created_at",
    )

    search_fields = (
        "response__response_no",
        "note",
    )

    autocomplete_fields = (
        "response",
        "created_by",
    )