from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils import timezone

from import_export.admin import ImportExportModelAdmin

from .forms import (
    CompanyAdminForm,
    BranchAdminForm,
)

from .resources import (
    CompanyResource,
    BranchResource,
    DepartmentResource,
    DesignationResource,
    CompanyContactResource,
    CompanyDocumentResource,
    CompanyGalleryResource,
)

from .models import (
    Company,
    Branch,
    Department,
    Designation,
    CompanyContact,
    CompanyDocument,
    CompanyGallery,
    CompanyStatus,
    CompanyIndustry,
    CompanyType,
    CompanySize,
    CompanyCategory,
    GoogleMapStatus,
    DocumentType,
)

#Base Admin
class MasterAdmin(ImportExportModelAdmin):
    ordering = ("name",)

    search_fields = ("name",)

    list_per_page = 25

    save_on_top = True

#Bulk Actions
@admin.action(description="Verify Selected Companies")
def verify_company(modeladmin, request, queryset):
    queryset.update(is_verified=True)


@admin.action(description="Remove Verification")
def unverify_company(modeladmin, request, queryset):
    queryset.update(is_verified=False)


@admin.action(description="Feature Selected Companies")
def feature_company(modeladmin, request, queryset):
    queryset.update(is_featured=True)


@admin.action(description="Remove Featured")
def unfeature_company(modeladmin, request, queryset):
    queryset.update(is_featured=False)


@admin.action(description="Activate Selected Companies")
def activate_company(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Deactivate Selected Companies")
def deactivate_company(modeladmin, request, queryset):
    queryset.update(is_active=False)



#Image Preview
class ImagePreviewMixin:

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        if not obj.logo:
            return "-"

        return format_html(
            '<a href="{0}" target="_blank">'
            '<img src="{0}" style="height:55px;border-radius:8px;">'
            '</a>',
            obj.logo.url,
        )


    

    @admin.display(description="Cover")

    def cover_preview(self, obj):

        if obj.cover_image:

            return format_html(
                '<img src="{}" style="height:50px;border-radius:8px;">',
                obj.cover_image.url,
            )

        return "-"


#Gallery Inline
class CompanyGalleryInline(admin.TabularInline):

    model = CompanyGallery

    extra = 1

    fields = (
        "image",
        "title",
        "sort_order",
    )


#Branch Inline
class BranchInline(admin.TabularInline):

    model = Branch

    extra = 0

    form = BranchAdminForm

    show_change_link = True

    autocomplete_fields = (
        "city",
        "locality",
        "area",
        "postal_code",
    )


#Department Inline
class DepartmentInline(admin.TabularInline):

    model = Department

    extra = 0

    show_change_link = True

#Contact Inline
class CompanyContactInline(admin.TabularInline):

    model = CompanyContact

    extra = 0

    show_change_link = True


#Document Inline
class CompanyDocumentInline(admin.TabularInline):

    model = CompanyDocument

    extra = 0

    show_change_link = True



#Company Admin Start
@admin.register(Company)
class CompanyAdmin(
    ImagePreviewMixin,
    ImportExportModelAdmin,
):

    resource_class = CompanyResource

    form = CompanyAdminForm

    save_on_top = True

    list_per_page = 30

    date_hierarchy = "created_at"

    ordering = ("name",)

    actions = (

        verify_company,

        unverify_company,

        feature_company,

        unfeature_company,

        activate_company,

        deactivate_company,

    )

    list_display = (
    "logo_preview",
    "rating_stars",
    "name",
    "phone_link",
    "email_link",
    "branch_count",
    "department_count",
    "contact_count",
    "document_count",
    "gallery_count",
    "status_badge",
    "verified_badge",
    "featured_badge",
    "active_badge",
)

    @admin.display(description="Rating")
    def rating_stars(self, obj):

        if obj.rating is None:
            return "-"

        stars = "⭐" * int(obj.rating)

        return format_html(
            "{} <small>({})</small>",
            stars,
            obj.rating,
        )


    list_display_links = (
        "name",
    )

    search_fields = (

        "name",

        "legal_name",

        "primary_phone",

        "email",

        "gst_number",

        "pan_number",

    )

    list_filter = (

        "status",

        "industry",

        "company_type",

        "company_size",

        "category",

        "city",

        "is_verified",

        "is_featured",

        "is_active",

        "created_at",

    )



    fieldsets = (

    (
        "📌 Basic Information",
        {
            "fields": (
                ("status", "assigned_to"),
                ("category",),
                ("name", "legal_name"),
                ("industry", "company_type"),
                ("company_size",),
                ("is_verified", "is_featured", "is_active"),
            )
        },
    ),

    (
        "📞 Contact Information",
        {
            "classes": ("collapse",),
            "fields": (
                ("primary_phone", "alternate_phone"),
                ("whatsapp", "email"),
                ("website",),
            ),
        },
    ),

    (
        "📍 Address",
        {
            "classes": ("collapse",),
            "fields": (
                ("city", "locality"),
                ("area", "postal_code"),
                ("address",),
                ("google_map",),
            ),
        },
    ),

    (
        "🏢 Business Information",
        {
            "classes": ("collapse",),
            "fields": (
                ("founded_year", "employee_strength"),
                ("gst_number", "pan_number"),
                ("cin_number",),
                ("rating", "reviews_count"),
                ("google_business_status",),
            ),
        },
    ),

    (
        "🖼 Branding",
        {
            "classes": ("collapse",),
            "fields": (
                ("logo", "logo_preview"),
                ("cover_image", "cover_preview"),
            ),
        },
    ),

    (
        "📝 Description",
        {
            "classes": ("collapse",),
            "fields": (
                "short_description",
                "about",
            ),
        },
    ),

    (
        "🌐 Social Media",
        {
            "classes": ("collapse",),
            "fields": (
                ("facebook", "instagram"),
                ("linkedin", "twitter"),
                ("youtube",),
            ),
        },
    ),

    (
        "🔍 SEO",
        {
            "classes": ("collapse",),
            "fields": (
                "meta_title",
                "meta_description",
                "meta_keywords",
            ),
        },
    ),

        (
        "🕒 Audit Information",
        {
            "classes": ("collapse",),
            "fields": (
                "slug",
                ("created_at", "updated_at"),
            ),
        },
    ),

)

    autocomplete_fields = (

        "industry",

        "company_type",

        "company_size",

        "category",

        "status",

        "assigned_to",

        "city",

        "locality",

        "area",

        "postal_code",

        "google_business_status",
        

    )

    readonly_fields = (

        "logo_preview",

        "cover_preview",

        "slug",

        "created_at",

        "updated_at",

    )

    inlines = (

        BranchInline,

        DepartmentInline,

        CompanyContactInline,

        CompanyDocumentInline,

        CompanyGalleryInline,

    )


    @admin.display(description="Created On", ordering="created_at")
    def created_date(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%d-%m-%Y %I:%M %p")
        return "-"


    @admin.display(description="Updated On", ordering="updated_at")
    def updated_date(self, obj):
        if obj.updated_at:
            return obj.updated_at.strftime("%d-%m-%Y %I:%M %p")
        return "-"


    def save_model(self, request, obj, form, change):

        if not change:
            obj.created_by = request.user

        obj.updated_by = request.user

        super().save_model(request, obj, form, change)




    @admin.display(description="Verified", ordering="is_verified")
    def verified_badge(self, obj):
        if obj.is_verified:
            return format_html(
            '<a href="{0}" target="_blank">'
            '<img src="{0}" style="height:50px;border-radius:8px;">'
            '</a>',
            obj.cover_image.url,
        )


    @admin.display(description="Featured", ordering="is_featured")
    def featured_badge(self, obj):
        if obj.is_featured:
            return format_html(
                '<span style="color:#f59e0b;font-size:18px;">★</span>'
            )
        return format_html(
            '<span style="color:#9ca3af;font-size:18px;">☆</span>'
        )


    @admin.display(description="Active", ordering="is_active")
    def active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color:#16a34a;font-weight:bold;">Active</span>'
            )
        return format_html(
                '<span style="color:#dc2626;font-weight:bold;">Inactive</span>'
        )


    @admin.display(description="Phone")
    def phone_link(self, obj):
        if not obj.primary_phone:
            return "-"
        return format_html(
            '<a href="tel:{}">{}</a>',
            obj.primary_phone,
            obj.primary_phone,
        )


    @admin.display(description="Email")
    def email_link(self, obj):
        if not obj.email:
            return "-"
        return format_html(
            '<a href="mailto:{}">{}</a>',
            obj.email,
            obj.email,
        )


    @admin.display(description="Website")
    def website_link(self, obj):
        if not obj.website:
            return "-"
        return format_html(
            '<a href="{}" target="_blank">🌐 Visit</a>',
            obj.website,
        )


    @admin.display(description="Map")
    def google_map_link(self, obj):
        if not obj.google_map:
            return "-"
        return format_html(
            '<a href="{}" target="_blank">📍 Open</a>',
            obj.google_map,
        )

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "status",
                "industry",
                "company_type",
                "company_size",
                "category",
                "assigned_to",
                "city",
                "locality",
                "area",
                "postal_code",
                "google_business_status",
            )
            .annotate(
                total_branches=Count("branches", distinct=True),
                total_departments=Count("departments", distinct=True),
                total_contacts=Count("contacts", distinct=True),
                total_documents=Count("documents", distinct=True),
                total_gallery=Count("gallery", distinct=True),
            )
        )


    @admin.display(description="Branches", ordering="total_branches")
    def branch_count(self, obj):
        return obj.total_branches


    @admin.display(description="Departments", ordering="total_departments")
    def department_count(self, obj):
        return obj.total_departments


    @admin.display(description="Contacts", ordering="total_contacts")
    def contact_count(self, obj):
        return obj.total_contacts


    @admin.display(description="Documents", ordering="total_documents")
    def document_count(self, obj):
        return obj.total_documents


    @admin.display(description="Gallery", ordering="total_gallery")
    def gallery_count(self, obj):
        return obj.total_gallery



    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):

        if not obj.status:
            return "-"

        colors = {
            "primary": "#0d6efd",
            "success": "#198754",
            "warning": "#ffc107",
            "danger": "#dc3545",
            "info": "#0dcaf0",
            "secondary": "#6c757d",
            "dark": "#212529",
        }

        color = colors.get(obj.status.color, obj.status.color)

        return format_html(
            '<span style="background:{};color:white;padding:4px 10px;border-radius:20px;font-weight:600;">{}</span>',
            color,
            obj.status.name,
        )
        

@admin.register(CompanyStatus)
class CompanyStatusAdmin(MasterAdmin):
    list_display = (
        "name",
        "color",
        "icon",
        "sort_order",
        "is_active",
    )


@admin.register(CompanyCategory)
class CompanyCategoryAdmin(MasterAdmin):
    list_display = (
        "name",
        "is_active",
    )


@admin.register(CompanyIndustry)
class CompanyIndustryAdmin(MasterAdmin):
    list_display = (
        "name",
        "is_active",
    )


@admin.register(CompanyType)
class CompanyTypeAdmin(MasterAdmin):
    list_display = (
        "name",
        "is_active",
    )


@admin.register(CompanySize)
class CompanySizeAdmin(MasterAdmin):
    list_display = (
        "name",
        "min_employee",
        "max_employee",
        "is_active",
    )


@admin.register(GoogleMapStatus)
class GoogleMapStatusAdmin(MasterAdmin):
    list_display = (
        "name",
        "is_active",
    )



