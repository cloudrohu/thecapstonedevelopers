from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin

from .models import (
    Job,
    JobApplicant,
    InterviewSchedule,
    OfferLetter,
    EmployeeJoining,
    JobActivityLog,
)

from .resources import (
    JobResource,
    JobApplicantResource,
    InterviewScheduleResource,
    OfferLetterResource,
    EmployeeJoiningResource,
)


# ==========================================================
# Common Admin Actions
# ==========================================================

@admin.action(description="Publish Selected Jobs")
def publish_jobs(modeladmin, request, queryset):
    updated = queryset.update(published=True)
    messages.success(request, f"{updated} jobs published successfully.")


@admin.action(description="Unpublish Selected Jobs")
def unpublish_jobs(modeladmin, request, queryset):
    updated = queryset.update(published=False)
    messages.success(request, f"{updated} jobs unpublished successfully.")


@admin.action(description="Mark Featured")
def make_featured(modeladmin, request, queryset):
    updated = queryset.update(featured=True)
    messages.success(request, f"{updated} jobs marked as featured.")


@admin.action(description="Remove Featured")
def remove_featured(modeladmin, request, queryset):
    updated = queryset.update(featured=False)
    messages.success(request, f"{updated} jobs updated.")


@admin.action(description="Activate Jobs")
def activate_jobs(modeladmin, request, queryset):
    updated = queryset.update(status="ACTIVE")
    messages.success(request, f"{updated} jobs activated.")


@admin.action(description="Pause Jobs")
def pause_jobs(modeladmin, request, queryset):
    updated = queryset.update(status="PAUSED")
    messages.success(request, f"{updated} jobs paused.")


@admin.action(description="Close Jobs")
def close_jobs(modeladmin, request, queryset):
    updated = queryset.update(status="CLOSED")
    messages.success(request, f"{updated} jobs closed.")


# ==========================================================
# Job Admin
# ==========================================================

@admin.register(Job)
class JobAdmin(ImportExportModelAdmin):

    resource_class = JobResource

    list_display = (
        "title",
        "company",
        "location",
        "vacancy",
        "status_badge",
        "featured_badge",
        "published_badge",
        "applicant_count",
        "interview_count",
        "offer_count",
        "created_at",
    )

    list_filter = (
        "company",
        "status",
        "featured",
        "published",
        "job_type",
        "work_mode",
        "category",
        "industry",
        "created_at",
    )

    search_fields = (
        "title__name",
        "company__name",
        "slug",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "company",
        "title",
        "category",
        "industry",
        "location",
        "postal_code",
    )

    filter_horizontal = (
        "skills",
        "benefits",
        "assets",
        "documents",
        "languages",
    )

    list_select_related = (
        "company",
        "title",
        "category",
        "industry",
        "location",
    )

    actions = (
        publish_jobs,
        unpublish_jobs,
        make_featured,
        remove_featured,
        activate_jobs,
        pause_jobs,
        close_jobs,
    )

    show_full_result_count = False

    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "company",
                    "title",
                    "slug",
                    "category",
                    "industry",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "location",
                    "postal_code",
                )
            },
        ),
        (
            "Employment",
            {
                "fields": (
                    "vacancy",
                    "job_type",
                    "work_mode",
                    "gender",
                    "qualification",
                )
            },
        ),
        (
            "Salary",
            {
                "fields": (
                    "salary_type",
                    "minimum_salary",
                    "maximum_salary",
                    "negotiable",
                    "hide_salary",
                )
            },
        ),
        (
            "Experience",
            {
                "fields": (
                    "minimum_experience",
                    "maximum_experience",
                    "minimum_age",
                    "maximum_age",
                )
            },
        ),
        (
            "Description",
            {
                "fields": (
                    "short_description",
                    "description",
                    "responsibilities",
                    "requirements",
                )
            },
        ),
        (
            "Skills",
            {
                "fields": (
                    "skills",
                    "benefits",
                    "assets",
                    "documents",
                    "languages",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "featured",
                    "published",
                    "status",
                    "expiry_date",
                )
            },
        ),
        (
            "SEO",
            {
                "classes": ("collapse",),
                "fields": (
                    "meta_title",
                    "meta_description",
                    "meta_keywords",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "company",
                "title",
                "category",
                "industry",
                "location",
            )
            .prefetch_related(
                "skills",
                "benefits",
            )
            .annotate(
                total_applicants=Count("applicants"),
                total_interviews=Count("interviews"),
                total_offers=Count("offer_letters"),
            )
        )


    # ==========================================================
    # BADGES
    # ==========================================================

    @admin.display(description="Status")
    def status_badge(self, obj):

        colors = {
            "DRAFT": "#6B7280",
            "ACTIVE": "#16A34A",
            "PAUSED": "#F59E0B",
            "CLOSED": "#DC2626",
            "EXPIRED": "#7C3AED",
        }

        color = colors.get(obj.status, "#6B7280")

        return format_html(
            '<span style="background:{};color:white;padding:4px 10px;'
            'border-radius:20px;font-size:12px;font-weight:600;">'
            '{}</span>',
            color,
            obj.get_status_display(),
        )

    @admin.display(description="Featured", ordering="featured")
    def featured_badge(self, obj):

        if obj.featured:
            return format_html(
                '<span style="color:#16A34A;font-weight:700;">✓ Featured</span>'
            )

        return format_html(
            '<span style="color:#9CA3AF;">—</span>'
        )

    @admin.display(description="Published", ordering="published")
    def published_badge(self, obj):

        if obj.published:
            return format_html(
                '<span style="color:#16A34A;font-weight:700;">Published</span>'
            )

        return format_html(
            '<span style="color:#DC2626;font-weight:700;">Hidden</span>'
        )

    # ==========================================================
    # COUNTERS
    # ==========================================================

    @admin.display(description="Applicants")
    def applicant_count(self, obj):
        return obj.total_applicants

    @admin.display(description="Interviews")
    def interview_count(self, obj):
        return obj.total_interviews

    @admin.display(description="Offers")
    def offer_count(self, obj):
        return obj.total_offers


# ==========================================================
# JOB APPLICANT ADMIN
# ==========================================================

@admin.register(JobApplicant)
class JobApplicantAdmin(ImportExportModelAdmin):

    resource_class = JobApplicantResource

    list_display = (
        "full_name",
        "phone_link",
        "email_link",
        "job",
        "current_company",
        "experience_display",
        "status_badge",
        "expected_salary_display",
        "resume_link",
        "applied_at",
    )

    list_filter = (
        "status",
        "source",
        "job",
        "applied_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
        "current_company",
    )

    ordering = ("-applied_at",)

    autocomplete_fields = (
        "job",
        "location",
        "postal_code",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "applied_at",
    )

    list_select_related = (
        "job",
        "location",
        "postal_code",
    )

    date_hierarchy = "applied_at"

    show_full_result_count = False

    fieldsets = (

        (
            "Applicant",
            {
                "fields": (
                    "job",
                    "full_name",
                    "image",
                    "phone",
                    "alternate_phone",
                    "email",
                )
            },
        ),

        (
            "Professional",
            {
                "fields": (
                    "current_company",
                    "current_designation",
                    "experience",
                    "current_salary",
                    "expected_salary",
                    "notice_period",
                    "expected_joining_date",
                )
            },
        ),

        (
            "Location",
            {
                "fields": (
                    "location",
                    "postal_code",
                )
            },
        ),

        (
            "Documents",
            {
                "fields": (
                    "resume",
                    "cover_letter",
                )
            },
        ),

        (
            "Application",
            {
                "fields": (
                    "source",
                    "status",
                    "allow_whatsapp",
                    "remarks",
                )
            },
        ),

    )

    actions = (
        "mark_shortlisted",
        "mark_selected",
        "mark_rejected",
    )

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "job",
                "location",
            )
        )

    @admin.display(description="Phone")
    def phone_link(self, obj):

        return format_html(
            '<a href="tel:{}">{}</a>',
            obj.phone,
            obj.phone,
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

    @admin.display(description="Resume")
    def resume_link(self, obj):

        if not obj.resume:
            return "-"

        return format_html(
            '<a href="{}" target="_blank">Download</a>',
            obj.resume.url,
        )

    @admin.display(description="Experience")
    def experience_display(self, obj):

        years = obj.experience // 12
        months = obj.experience % 12

        return f"{years}Y {months}M"

    @admin.display(description="Expected Salary")
    def expected_salary_display(self, obj):

        return f"${obj.expected_salary:,.2f}"

    @admin.display(description="Status")
    def status_badge(self, obj):

        colors = {
            "APPLIED": "#2563EB",
            "SHORTLISTED": "#16A34A",
            "INTERVIEW": "#9333EA",
            "SELECTED": "#0F766E",
            "REJECTED": "#DC2626",
            "HOLD": "#D97706",
            "JOINED": "#15803D",
        }

        color = colors.get(obj.status, "#6B7280")

        return format_html(
            '<span style="background:{};color:white;padding:4px 10px;'
            'border-radius:20px;font-size:12px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    @admin.action(description="Mark Selected")
    def mark_selected(self, request, queryset):
        updated = queryset.update(status="SELECTED")
        self.message_user(request, f"{updated} applicants updated.")

    @admin.action(description="Mark Shortlisted")
    def mark_shortlisted(self, request, queryset):
        updated = queryset.update(status="SHORTLISTED")
        self.message_user(request, f"{updated} applicants updated.")

    @admin.action(description="Mark Rejected")
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status="REJECTED")
        self.message_user(request, f"{updated} applicants updated.")

# ==========================================================
# INTERVIEW SCHEDULE ADMIN
# ==========================================================

@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(ImportExportModelAdmin):

    resource_class = InterviewScheduleResource

    list_display = (
        "applicant",
        "job",
        "interview_type_badge",
        "scheduled_datetime",
        "interviewer",
        "status_badge",
        "meeting_link_button",
        "whatsapp_badge",
    )

    list_filter = (
        "interview_type",
        "status",
        "scheduled_datetime",
        "job",
    )

    search_fields = (
        "applicant__full_name",
        "job__title__name",
        "interviewer",
    )

    autocomplete_fields = (
        "job",
        "applicant",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-scheduled_datetime",
    )

    date_hierarchy = "scheduled_datetime"

    list_select_related = (
        "job",
        "applicant",
    )

    fieldsets = (

        (
            "Interview",
            {
                "fields": (
                    "job",
                    "applicant",
                    "interview_type",
                    "scheduled_datetime",
                    "duration",
                )
            },
        ),

        (
            "Interviewer",
            {
                "fields": (
                    "interviewer",
                    "office_address",
                    "meeting_link",
                )
            },
        ),

        (
            "Status",
            {
                "fields": (
                    "status",
                    "feedback",
                    "internal_notes",
                )
            },
        ),

        (
            "Notification",
            {
                "fields": (
                    "whatsapp_sent",
                    "reminder_sent",
                )
            },
        ),

    )

    @admin.display(description="Meeting")

    def meeting_link_button(self, obj):

        if not obj.meeting_link:
            return "-"

        return format_html(
            '<a class="button" target="_blank" href="{}">Open</a>',
            obj.meeting_link,
        )

    @admin.display(description="WhatsApp")

    def whatsapp_badge(self, obj):

        if obj.whatsapp_sent:
            return format_html(
                '<span style="color:#16A34A;font-weight:bold;">Sent</span>'
            )

        return format_html(
            '<span style="color:#DC2626;">Pending</span>'
        )

    @admin.display(description="Interview")

    def interview_type_badge(self, obj):

        return format_html(
            '<strong>{}</strong>',
            obj.get_interview_type_display(),
        )

    @admin.display(description="Status")

    def status_badge(self, obj):

        colors = {
            "SCHEDULED": "#2563EB",
            "CONFIRMED": "#16A34A",
            "COMPLETED": "#059669",
            "CANCELLED": "#DC2626",
            "RESCHEDULED": "#D97706",
            "NO_SHOW": "#7C3AED",
        }

        color = colors.get(obj.status, "#6B7280")

        return format_html(
            '<span style="background:{};color:white;'
            'padding:4px 10px;border-radius:20px;">'
            '{}'
            '</span>',
            color,
            obj.get_status_display(),
        )


# ==========================================================
# OFFER LETTER ADMIN
# ==========================================================

@admin.register(OfferLetter)
class OfferLetterAdmin(ImportExportModelAdmin):

    resource_class = OfferLetterResource

    list_display = (
        "offer_number",
        "applicant",
        "designation",
        "annual_ctc_display",
        "joining_date",
        "status_badge",
        "download_offer",
    )

    list_filter = (
        "status",
        "joining_date",
        "offer_date",
    )

    search_fields = (
        "offer_number",
        "designation",
        "applicant__full_name",
    )

    autocomplete_fields = (
        "job",
        "applicant",
        "work_location",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-offer_date",
    )

    @admin.display(description="Annual CTC")

    def annual_ctc_display(self, obj):

        return f"${obj.annual_ctc:,.2f}"

    @admin.display(description="Offer")

    def download_offer(self, obj):

        if not obj.attachment:
            return "-"

        return format_html(
            '<a href="{}" target="_blank">Download</a>',
            obj.attachment.url,
        )

    @admin.display(description="Status")

    def status_badge(self, obj):

        colors = {
            "DRAFT": "#6B7280",
            "GENERATED": "#2563EB",
            "SENT": "#0EA5E9",
            "ACCEPTED": "#16A34A",
            "REJECTED": "#DC2626",
            "EXPIRED": "#D97706",
            "CANCELLED": "#991B1B",
        }

        color = colors.get(obj.status, "#6B7280")

        return format_html(
            '<span style="background:{};color:white;'
            'padding:4px 10px;border-radius:20px;">'
            '{}'
            '</span>',
            color,
            obj.get_status_display(),
        )



# ==========================================================
# EMPLOYEE JOINING ADMIN
# ==========================================================

@admin.register(EmployeeJoining)
class EmployeeJoiningAdmin(ImportExportModelAdmin):

    resource_class = EmployeeJoiningResource

    list_display = (
        "employee_code",
        "applicant",
        "designation",
        "department",
        "manager",
        "joining_date",
        "status_badge",
        "documents_badge",
        "welcome_badge",
    )

    list_filter = (
        "status",
        "joining_date",
        "documents_verified",
        "welcome_mail_sent",
        "onboarding_completed",
    )

    search_fields = (
        "employee_code",
        "designation",
        "department",
        "manager",
        "applicant__full_name",
    )

    autocomplete_fields = (
        "applicant",
        "offer_letter",
        "work_location",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-joining_date",
    )

    list_select_related = (
        "applicant",
        "offer_letter",
        "work_location",
    )

    fieldsets = (

        (
            "Employee",
            {
                "fields": (
                    "employee_code",
                    "applicant",
                    "offer_letter",
                )
            },
        ),

        (
            "Employment",
            {
                "fields": (
                    "designation",
                    "department",
                    "manager",
                    "work_location",
                )
            },
        ),

        (
            "Dates",
            {
                "fields": (
                    "joining_date",
                    "confirmation_date",
                )
            },
        ),

        (
            "Onboarding",
            {
                "fields": (
                    "documents_verified",
                    "id_card_issued",
                    "welcome_mail_sent",
                    "onboarding_completed",
                )
            },
        ),

        (
            "Other",
            {
                "fields": (
                    "status",
                    "remarks",
                )
            },
        ),
    )

    @admin.display(description="Status")
    def status_badge(self, obj):

        colors = {
            "PENDING": "#D97706",
            "DOCUMENT_PENDING": "#2563EB",
            "JOINED": "#16A34A",
            "CANCELLED": "#DC2626",
        }

        color = colors.get(obj.status, "#6B7280")

        return format_html(
            '<span style="background:{};color:#fff;'
            'padding:4px 10px;border-radius:20px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    @admin.display(description="Documents")
    def documents_badge(self, obj):

        if obj.documents_verified:
            return format_html(
                '<span style="color:#16A34A;font-weight:700;">Verified</span>'
            )

        return format_html(
            '<span style="color:#DC2626;">Pending</span>'
        )

    @admin.display(description="Welcome")
    def welcome_badge(self, obj):

        if obj.welcome_mail_sent:
            return format_html(
                '<span style="color:#16A34A;">Sent</span>'
            )

        return format_html(
            '<span style="color:#D97706;">Pending</span>'
        )


# ==========================================================
# JOB ACTIVITY LOG ADMIN
# ==========================================================

@admin.register(JobActivityLog)
class JobActivityLogAdmin(admin.ModelAdmin):

    list_display = (
        "job",
        "applicant",
        "activity_badge",
        "title",
        "created_at",
    )

    search_fields = (
        "job__title__name",
        "applicant__full_name",
        "title",
        "description",
    )

    list_filter = (
        "activity",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    readonly_fields = (
        "job",
        "applicant",
        "activity",
        "title",
        "description",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description="Activity")
    def activity_badge(self, obj):

        colors = {
            "CREATED": "#2563EB",
            "UPDATED": "#D97706",
            "APPLIED": "#16A34A",
            "SHORTLISTED": "#9333EA",
            "INTERVIEW": "#0891B2",
            "OFFER": "#7C3AED",
            "JOINED": "#15803D",
            "REJECTED": "#DC2626",
        }

        color = colors.get(obj.activity, "#6B7280")

        return format_html(
            '<span style="background:{};color:#fff;'
            'padding:4px 10px;border-radius:20px;">{}</span>',
            color,
            obj.get_activity_display(),
        )