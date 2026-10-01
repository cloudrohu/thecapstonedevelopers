from django.contrib import admin

from apps.enquiries.models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "enquiry_no",
        "customer",
        "source",
        "status",
        "assigned_to",
        "enquiry_date",
        "created_at",
    )

    list_display_links = (
        "enquiry_no",
        "customer",
    )

    list_filter = (
        "status",
        "source",
        "assigned_to",
        "created_at",
    )

    search_fields = (
        "enquiry_no",
        "customer__name",
        "customer__mobile",
        "customer__email",
    )

    autocomplete_fields = (
        "customer",
        "source",
        "status",
        "assigned_to",
    )

    readonly_fields = (
        "enquiry_no",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_select_related = (
        "customer",
        "source",
        "status",
        "assigned_to",
    )

    fieldsets = (
        (
            "Enquiry Information",
            {
                "fields": (
                    "enquiry_no",
                    "customer",
                    "source",
                    "status",
                    "assigned_to",
                )
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "subject",
                    "description",
                    "expected_budget",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "enquiry_date",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
                "enquiry_no",
                "enquiry_date",
                "created_at",
                "updated_at",
            )

        return (
            "enquiry_no",
            "created_at",
            "updated_at",
        )

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.fieldsets

        return (
            (
                "Enquiry Information",
                {
                    "fields": (
                        "enquiry_no",
                        "customer",
                        "source",
                        "status",
                        "assigned_to",
                    )
                },
            ),
            (
                "Details",
                {
                    "fields": (
                        "subject",
                        "description",
                        "expected_budget",
                    )
                },
            ),
            (
                "Dates",
                {
                    "fields": (
                        "enquiry_date",
                    )
                },
            ),
        )