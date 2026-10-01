from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin

from apps.business.models import Business
from apps.business.resources import BusinessResource

from .inlines import (
    BusinessGalleryInline,
    BusinessTimingInline,
    BusinessHolidayInline,
    BusinessDocumentInline,
    BusinessSocialLinkInline,
    BusinessAttributeValueInline,
)


@admin.register(Business)
class BusinessAdmin(ImportExportModelAdmin):

    resource_class = BusinessResource

    save_on_top = True

    save_as = True

    list_per_page = 30

    list_max_show_all = 50

    date_hierarchy = "created_at"

    empty_value_display = "-"

    prepopulated_fields = {
        "slug": (
            "name",
        ),
    }

    list_display = (
        "logo_preview",
        "name",
        "category",
        "business_type",
        "location",
        "phone",
        "rating_badge",
        "views_badge",
        "verified_badge",
        "featured_badge",
        "premium_badge",
        "is_active",
    )

    list_display_links = (
        "name",
    )

    search_fields = (
        "name",
        "code",
        "slug",
        "phone",
        "whatsapp",
        "email",
        "website",
        "owner_name",
    )

    list_filter = (
        "category",
        "business_type",
        "chain",
        "location",
        "is_verified",
        "is_featured",
        "is_premium",
        "is_active",
    )

    ordering = (
        "name",
    )

    list_select_related = (
        "category",
        "business_type",
        "chain",
        "location",
    )




    readonly_fields = (
        "logo_preview",
        "cover_preview",
        "created_at",
        "updated_at",
    )

    inlines = (
        BusinessGalleryInline,
        BusinessTimingInline,
        BusinessHolidayInline,
        BusinessDocumentInline,
        BusinessSocialLinkInline,
        BusinessAttributeValueInline,
    )

    @admin.display(description="Logo")
    def logo_preview(self, obj):

        if obj.logo:
            return format_html(
                '<img src="{}" '
                'style="width:60px;height:60px;'
                'border-radius:8px;'
                'object-fit:cover;" />',
                obj.logo.url,
            )

        return "-"

    @admin.display(description="Cover")
    def cover_preview(self, obj):

        if obj.cover_image:
            return format_html(
                '<img src="{}" '
                'style="width:180px;'
                'border-radius:8px;" />',
                obj.cover_image.url,
            )

        return "-"

    @admin.display(description="Rating")
    def rating_badge(self, obj):

        return format_html(
            "<strong>{:.2f} ⭐</strong>",
            obj.rating,
        )

    @admin.display(description="Views")
    def views_badge(self, obj):

        return format_html(
            "{} 👁",
            obj.view_count,
        )

    @admin.display(description="Verified")
    def verified_badge(self, obj):

        if obj.is_verified:
            return format_html(
                '<span style="background:#198754;'
                'color:white;padding:4px 10px;'
                'border-radius:20px;">'
                '✓ Verified'
                '</span>'
            )

        return format_html(
            '<span style="background:#dc3545;'
            'color:white;padding:4px 10px;'
            'border-radius:20px;">'
            '✗ No'
            '</span>'
        )

    @admin.display(description="Featured")
    def featured_badge(self, obj):

        if obj.is_featured:
            return format_html(
                '<span style="background:#fd7e14;'
                'color:white;padding:4px 10px;'
                'border-radius:20px;">'
                '⭐ Featured'
                '</span>'
            )

        return "-"

    @admin.display(description="Premium")
    def premium_badge(self, obj):

        if obj.is_premium:
            return format_html(
                '<span style="background:#6f42c1;'
                'color:white;padding:4px 10px;'
                'border-radius:20px;">'
                '💎 Premium'
                '</span>'
            )

        return "-"


        fieldsets = (

        (
            "Basic Information",
            {
                "fields": (
                    "category",
                    "business_type",
                    "chain",
                    "name",
                    "code",
                    "slug",
                    "short_description",
                    "description",
                )
            },
        ),

        (
            "Contact Information",
            {
                "fields": (
                    "owner_name",
                    "phone",
                    "whatsapp",
                    "email",
                    "website",
                )
            },
        ),

        (
            "Location",
            {
                "fields": (
                    "location",
                    "address",
                    (
                        "latitude",
                        "longitude",
                    ),
                )
            },
        ),

        (
            "Media",
            {
                "fields": (
                    "logo",
                    "logo_preview",
                    "cover_image",
                    "cover_preview",
                )
            },
        ),

        (
            "Business Details",
            {
                "fields": (
                    "gst_number",
                    "pan_number",
                    "established_year",
                    "employee_count",
                )
            },
        ),

        (
            "Features",
            {
                "fields": (
                    "amenities",
                    "services",
                    "tags",
                    "payment_methods",
                    "languages",
                )
            },
        ),

        (
            "Status",
            {
                "fields": (
                    "is_verified",
                    "is_featured",
                    "is_premium",
                    "is_active",
                )
            },
        ),

        (
            "Statistics",
            {
                "fields": (
                    "rating",
                    "review_count",
                    "view_count",
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

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "category",
                "business_type",
                "chain",
                "location",
            )
            .prefetch_related(
                "amenities",
                "services",
                "tags",
                "payment_methods",
                "languages",
                "gallery",
                "documents",
                "social_links",
                "attribute_values",
            )
        )


        # ==========================================================
    # Admin Actions
    # ==========================================================

    actions = (
        "verify_business",
        "unverify_business",
        "make_featured",
        "remove_featured",
        "make_premium",
        "remove_premium",
        "activate_business",
        "deactivate_business",
        "reset_views",
        "reset_reviews",
    )

    @admin.action(description="✅ Verify Selected Businesses")
    def verify_business(self, request, queryset):

        count = queryset.update(
            is_verified=True,
        )

        self.message_user(
            request,
            f"{count} business(es) verified successfully.",
        )

    @admin.action(description="❌ Remove Verification")
    def unverify_business(self, request, queryset):

        count = queryset.update(
            is_verified=False,
        )

        self.message_user(
            request,
            f"{count} business(es) unverified successfully.",
        )

    @admin.action(description="⭐ Mark as Featured")
    def make_featured(self, request, queryset):

        count = queryset.update(
            is_featured=True,
        )

        self.message_user(
            request,
            f"{count} business(es) marked as featured.",
        )

    @admin.action(description="Remove Featured")
    def remove_featured(self, request, queryset):

        count = queryset.update(
            is_featured=False,
        )

        self.message_user(
            request,
            f"{count} business(es) removed from featured.",
        )

    @admin.action(description="💎 Mark as Premium")
    def make_premium(self, request, queryset):

        count = queryset.update(
            is_premium=True,
        )

        self.message_user(
            request,
            f"{count} business(es) marked as premium.",
        )

    @admin.action(description="Remove Premium")
    def remove_premium(self, request, queryset):

        count = queryset.update(
            is_premium=False,
        )

        self.message_user(
            request,
            f"{count} business(es) removed from premium.",
        )

    @admin.action(description="✅ Activate Businesses")
    def activate_business(self, request, queryset):

        count = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            f"{count} business(es) activated.",
        )

    @admin.action(description="❌ Deactivate Businesses")
    def deactivate_business(self, request, queryset):

        count = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            f"{count} business(es) deactivated.",
        )

    @admin.action(description="👁 Reset View Counter")
    def reset_views(self, request, queryset):

        count = queryset.update(
            view_count=0,
        )

        self.message_user(
            request,
            f"View counter reset for {count} business(es).",
        )

    @admin.action(description="⭐ Reset Rating & Reviews")
    def reset_reviews(self, request, queryset):

        count = queryset.update(
            rating=0,
            review_count=0,
        )

        self.message_user(
            request,
            f"Rating reset for {count} business(es).",
        )

    # ==========================================================
    # Save Model
    # ==========================================================

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

    # ==========================================================
    # Save Messages
    # ==========================================================

    def response_add(self, request, obj, post_url_continue=None):

        self.message_user(
            request,
            f'"{obj}" created successfully.',
        )

        return super().response_add(
            request,
            obj,
            post_url_continue,
        )

    def response_change(self, request, obj):

        self.message_user(
            request,
            f'"{obj}" updated successfully.',
        )

        return super().response_change(
            request,
            obj,
        )


    