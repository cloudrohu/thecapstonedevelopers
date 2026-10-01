from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin



from apps.business.models.enquiry import (
    BusinessEnquiry,
    EnquiryStatus,
    EnquiryPriority,
)
from apps.business.resources import (
    BusinessEnquiryResource,
)


@admin.register(BusinessEnquiry)
class BusinessEnquiryAdmin(ImportExportModelAdmin):

    resource_class = BusinessEnquiryResource

    save_on_top = True

    save_as = True

    list_per_page = 50

    list_max_show_all = 500

    date_hierarchy = "created_at"

    empty_value_display = "-"

    autocomplete_fields = (
        "business",
        "assigned_to",
    )

    list_select_related = (
        "business",
        "assigned_to",
    )

    list_display = (
        "customer_name",
        "business",
        "phone",
        "source",
        "priority_badge",
        "status_badge",
        "assigned_to",
        "expected_close_date",
        "created_at",
    )

    list_display_links = (
        "customer_name",
    )

    search_fields = (
        "customer_name",
        "company_name",
        "phone",
        "whatsapp",
        "email",
        "business__name",
    )

    list_filter = (
        "source",
        "priority",
        "status",
        "assigned_to",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Business",
            {
                "fields": (
                    "business",
                )
            },
        ),

        (
            "Customer Information",
            {
                "fields": (
                    "customer_name",
                    "company_name",
                    "phone",
                    "whatsapp",
                    "email",
                )
            },
        ),

        (
            "Enquiry Details",
            {
                "fields": (
                    "source",
                    "priority",
                    "status",
                    "budget",
                    "requirement",
                )
            },
        ),

        (
            "Assignment",
            {
                "fields": (
                    "assigned_to",
                    "expected_close_date",
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

    @admin.display(description="Priority")
    def priority_badge(self, obj):

        colors = {
            EnquiryPriority.LOW: "#6c757d",
            EnquiryPriority.MEDIUM: "#0d6efd",
            EnquiryPriority.HIGH: "#fd7e14",
            EnquiryPriority.URGENT: "#dc3545",
        }

        return format_html(
            '<span style="background:{};'
            'color:white;'
            'padding:4px 10px;'
            'border-radius:15px;">'
            '{}'
            '</span>',
            colors.get(obj.priority, "#6c757d"),
            obj.get_priority_display(),
        )

    @admin.display(description="Status")
    def status_badge(self, obj):

        colors = {
            EnquiryStatus.NEW: "#0d6efd",
            EnquiryStatus.CONTACTED: "#fd7e14",
            EnquiryStatus.QUALIFIED: "#20c997",
            EnquiryStatus.CONVERTED: "#198754",
            EnquiryStatus.LOST: "#dc3545",
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
        "mark_contacted",
        "mark_qualified",
        "mark_converted",
        "mark_lost",
    )

    @admin.action(description="📞 Mark as Contacted")
    def mark_contacted(self, request, queryset):

        count = queryset.update(
            status=EnquiryStatus.CONTACTED,
        )

        self.message_user(
            request,
            f"{count} enquiry(s) marked as contacted.",
        )

    @admin.action(description="✅ Mark as Qualified")
    def mark_qualified(self, request, queryset):

        count = queryset.update(
            status=EnquiryStatus.QUALIFIED,
        )

        self.message_user(
            request,
            f"{count} enquiry(s) marked as qualified.",
        )

    @admin.action(description="🎉 Mark as Converted")
    def mark_converted(self, request, queryset):

        count = queryset.update(
            status=EnquiryStatus.CONVERTED,
        )

        self.message_user(
            request,
            f"{count} enquiry(s) converted.",
        )

    @admin.action(description="❌ Mark as Lost")
    def mark_lost(self, request, queryset):

        count = queryset.update(
            status=EnquiryStatus.LOST,
        )

        self.message_user(
            request,
            f"{count} enquiry(s) marked as lost.",
        )

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "business",
                "assigned_to",
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