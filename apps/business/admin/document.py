from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from apps.business.models import BusinessDocument
from apps.business.resources import BusinessDocumentResource


@admin.register(BusinessDocument)
class BusinessDocumentAdmin(ImportExportModelAdmin):

    resource_class = BusinessDocumentResource

    save_on_top = True

    save_as = True

    list_per_page = 50

    list_max_show_all = 500

    date_hierarchy = "created_at"

    empty_value_display = "-"

    autocomplete_fields = (
        "business",
        "document_type",
    )

    list_select_related = (
        "business",
        "document_type",
    )

    list_display = (
        "business",
        "document_type",
        "document_number",
        "verification_status",
        "issue_date",
        "expiry_date",
        "is_active",
    )

    list_display_links = (
        "document_type",
    )

    search_fields = (
        "business__name",
        "document_number",
        "document_type__name",
    )

    list_filter = (
        "verification_status",
        "document_type",
        "is_active",
    )

    ordering = (
        "business",
        "document_type",
    )

    readonly_fields = (
        "document_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Business",
            {
                "fields": (
                    "business",
                    "document_type",
                )
            },
        ),

        (
            "Document Information",
            {
                "fields": (
                    "document_number",
                    "document",
                    "document_preview",
                    (
                        "issue_date",
                        "expiry_date",
                    ),
                )
            },
        ),

        (
            "Verification",
            {
                "fields": (
                    "verification_status",
                    "remarks",
                )
            },
        ),

        (
            "Status",
            {
                "fields": (
                    "is_active",
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

    @admin.display(description="Document")
    def document_preview(self, obj):

        if obj.document:
            return format_html(
                '<a href="{}" target="_blank">View Document</a>',
                obj.document.url,
            )

        return "-"

    actions = (
        "approve_documents",
        "reject_documents",
        "mark_pending",
        "make_active",
        "make_inactive",
    )

    @admin.action(description="✅ Approve Selected Documents")
    def approve_documents(self, request, queryset):

        count = queryset.update(
            verification_status="APPROVED",
        )

        self.message_user(
            request,
            f"{count} document(s) approved.",
        )

    @admin.action(description="❌ Reject Selected Documents")
    def reject_documents(self, request, queryset):

        count = queryset.update(
            verification_status="REJECTED",
        )

        self.message_user(
            request,
            f"{count} document(s) rejected.",
        )

    @admin.action(description="⏳ Mark as Pending")
    def mark_pending(self, request, queryset):

        count = queryset.update(
            verification_status="PENDING",
        )

        self.message_user(
            request,
            f"{count} document(s) marked as pending.",
        )

    @admin.action(description="✅ Activate")
    def make_active(self, request, queryset):

        queryset.update(
            is_active=True,
        )

    @admin.action(description="❌ Deactivate")
    def make_inactive(self, request, queryset):

        queryset.update(
            is_active=False,
        )

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "business",
                "document_type",
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