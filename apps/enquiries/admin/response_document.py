from django.contrib import admin

from apps.enquiries.models import ResponseDocument


class ResponseDocumentInline(admin.TabularInline):
    model = ResponseDocument
    extra = 0

    fields = (
        "title",
        "document_type",
        "file",
        "uploaded_by",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "uploaded_by",
    )


@admin.register(ResponseDocument)
class ResponseDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "response",
        "document_type",
        "uploaded_by",
        "created_at",
    )

    list_filter = (
        "document_type",
    )

    search_fields = (
        "title",
        "response__response_no",
    )

    autocomplete_fields = (
        "response",
        "uploaded_by",
    )