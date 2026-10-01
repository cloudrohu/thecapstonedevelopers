from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin

from apps.business.models import (
    BusinessReview,
    ReviewStatus,
)
from apps.business.resources import (
    BusinessReviewResource,
)


@admin.register(BusinessReview)
class BusinessReviewAdmin(ImportExportModelAdmin):

    resource_class = BusinessReviewResource

    save_on_top = True

    save_as = True

    list_per_page = 50

    list_max_show_all = 500

    date_hierarchy = "created_at"

    empty_value_display = "-"

    autocomplete_fields = (
        "business",
    )

    list_select_related = (
        "business",
    )

    list_display = (
        "business",
        "reviewer_name",
        "rating_badge",
        "status_badge",
        "verified_badge",
        "created_at",
    )

    list_display_links = (
        "reviewer_name",
    )

    search_fields = (
        "business__name",
        "reviewer_name",
        "reviewer_email",
        "reviewer_phone",
        "title",
        "review",
    )

    list_filter = (
        "status",
        "is_verified",
        "rating",
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
            "Reviewer",
            {
                "fields": (
                    "reviewer_name",
                    "reviewer_email",
                    "reviewer_phone",
                )
            },
        ),

        (
            "Review",
            {
                "fields": (
                    "rating",
                    "title",
                    "review",
                )
            },
        ),

        (
            "Moderation",
            {
                "fields": (
                    "status",
                    "is_verified",
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

    @admin.display(description="Rating")
    def rating_badge(self, obj):

        return format_html(
            "<strong>{}/5 ⭐</strong>",
            obj.rating,
        )

    @admin.display(description="Status")
    def status_badge(self, obj):

        colors = {
            ReviewStatus.APPROVED: "#198754",
            ReviewStatus.PENDING: "#ffc107",
            ReviewStatus.REJECTED: "#dc3545",
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

    @admin.display(description="Verified")
    def verified_badge(self, obj):

        if obj.is_verified:
            return format_html(
                '<span style="color:green;font-weight:bold;">✔</span>'
            )

        return format_html(
            '<span style="color:red;font-weight:bold;">✘</span>'
        )

    actions = (
        "approve_reviews",
        "reject_reviews",
        "mark_pending",
        "verify_reviews",
        "unverify_reviews",
    )

    @admin.action(description="✅ Approve Selected Reviews")
    def approve_reviews(self, request, queryset):

        count = queryset.update(
            status=ReviewStatus.APPROVED,
        )

        self.message_user(
            request,
            f"{count} review(s) approved.",
        )

    @admin.action(description="❌ Reject Selected Reviews")
    def reject_reviews(self, request, queryset):

        count = queryset.update(
            status=ReviewStatus.REJECTED,
        )

        self.message_user(
            request,
            f"{count} review(s) rejected.",
        )

    @admin.action(description="⏳ Mark as Pending")
    def mark_pending(self, request, queryset):

        count = queryset.update(
            status=ReviewStatus.PENDING,
        )

        self.message_user(
            request,
            f"{count} review(s) marked as pending.",
        )

    @admin.action(description="✔ Verify Selected Reviews")
    def verify_reviews(self, request, queryset):

        count = queryset.update(
            is_verified=True,
        )

        self.message_user(
            request,
            f"{count} review(s) verified.",
        )

    @admin.action(description="✘ Unverify Selected Reviews")
    def unverify_reviews(self, request, queryset):

        count = queryset.update(
            is_verified=False,
        )

        self.message_user(
            request,
            f"{count} review(s) unverified.",
        )

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "business",
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