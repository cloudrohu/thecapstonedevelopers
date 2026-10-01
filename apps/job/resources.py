from import_export import fields, resources
from import_export.widgets import (
    ForeignKeyWidget,
    ManyToManyWidget,
    DateWidget,
)

from .models import (
    Job,
    JobApplicant,
    InterviewSchedule,
    OfferLetter,
    EmployeeJoining,
)

from apps.companies.models import Company
from apps.utility.models import Location, PostalCode

from apps.job_utility.models import (
    JobTitle,
    JobCategory,
    JobIndustry,
    JobSkill,
    JobBenefit,
    JobAsset,
    JobDocument,
    JobLanguageRequirement,
    SalaryType,
    WorkingDaysOption,
    JobTimingTemplate,
)


# ==========================================================
# JOB RESOURCE
# ==========================================================

class JobResource(resources.ModelResource):

    company = fields.Field(
        column_name="company",
        attribute="company",
        widget=ForeignKeyWidget(
            Company,
            "name",
        ),
    )

    title = fields.Field(
        column_name="title",
        attribute="title",
        widget=ForeignKeyWidget(
            JobTitle,
            "name",
        ),
    )

    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(
            JobCategory,
            "name",
        ),
    )

    industry = fields.Field(
        column_name="industry",
        attribute="industry",
        widget=ForeignKeyWidget(
            JobIndustry,
            "name",
        ),
    )

    location = fields.Field(
        column_name="location",
        attribute="location",
        widget=ForeignKeyWidget(
            Location,
            "name",
        ),
    )

    postal_code = fields.Field(
        column_name="postal_code",
        attribute="postal_code",
        widget=ForeignKeyWidget(
            PostalCode,
            "postal_code",
        ),
    )

    salary_type = fields.Field(
        column_name="salary_type",
        attribute="salary_type",
        widget=ForeignKeyWidget(
            SalaryType,
            "name",
        ),
    )

    working_days = fields.Field(
        column_name="working_days",
        attribute="working_days",
        widget=ForeignKeyWidget(
            WorkingDaysOption,
            "name",
        ),
    )

    timing = fields.Field(
        column_name="timing",
        attribute="timing",
        widget=ForeignKeyWidget(
            JobTimingTemplate,
            "name",
        ),
    )

    skills = fields.Field(
        column_name="skills",
        attribute="skills",
        widget=ManyToManyWidget(
            JobSkill,
            field="name",
            separator=",",
        ),
    )

    benefits = fields.Field(
        column_name="benefits",
        attribute="benefits",
        widget=ManyToManyWidget(
            JobBenefit,
            field="name",
            separator=",",
        ),
    )

    assets = fields.Field(
        column_name="assets",
        attribute="assets",
        widget=ManyToManyWidget(
            JobAsset,
            field="name",
            separator=",",
        ),
    )

    documents = fields.Field(
        column_name="documents",
        attribute="documents",
        widget=ManyToManyWidget(
            JobDocument,
            field="name",
            separator=",",
        ),
    )

    languages = fields.Field(
        column_name="languages",
        attribute="languages",
        widget=ManyToManyWidget(
            JobLanguageRequirement,
            field="name",
            separator=",",
        ),
    )

    expiry_date = fields.Field(
        column_name="expiry_date",
        attribute="expiry_date",
        widget=DateWidget(format="%Y-%m-%d"),
    )

    class Meta:

        model = Job

        skip_unchanged = True

        report_skipped = True

        use_bulk = True

        batch_size = 500

        import_id_fields = ("slug",)

        fields = (
            "id",
            "company",
            "title",
            "category",
            "industry",
            "location",
            "postal_code",
            "slug",
            "vacancy",
            "job_type",
            "work_mode",
            "gender",
            "minimum_age",
            "maximum_age",
            "minimum_experience",
            "maximum_experience",
            "qualification",
            "salary_type",
            "minimum_salary",
            "maximum_salary",
            "negotiable",
            "hide_salary",
            "working_days",
            "timing",
            "skills",
            "benefits",
            "assets",
            "documents",
            "languages",
            "featured",
            "published",
            "status",
            "expiry_date",
            "created_at",
        )

        export_order = fields



# ==========================================================
# JOB APPLICANT RESOURCE
# ==========================================================

class JobApplicantResource(resources.ModelResource):

    job = fields.Field(
        column_name="job",
        attribute="job",
        widget=ForeignKeyWidget(
            Job,
            "slug",
        ),
    )

    location = fields.Field(
        column_name="location",
        attribute="location",
        widget=ForeignKeyWidget(
            Location,
            "name",
        ),
    )

    postal_code = fields.Field(
        column_name="postal_code",
        attribute="postal_code",
        widget=ForeignKeyWidget(
            PostalCode,
            "postal_code",
        ),
    )

    applied_at = fields.Field(
        column_name="applied_at",
        attribute="applied_at",
        widget=DateWidget(format="%Y-%m-%d"),
    )

    class Meta:

        model = JobApplicant

        skip_unchanged = True

        report_skipped = True

        use_bulk = True

        batch_size = 500

        import_id_fields = (
            "job",
            "phone",
        )

        fields = (
            "id",
            "job",
            "full_name",
            "phone",
            "alternate_phone",
            "email",
            "current_company",
            "current_designation",
            "experience",
            "current_salary",
            "expected_salary",
            "notice_period",
            "expected_joining_date",
            "location",
            "postal_code",
            "source",
            "status",
            "allow_whatsapp",
            "remarks",
            "applied_at",
            "created_at",
        )

        export_order = fields


# ==========================================================
# INTERVIEW RESOURCE
# ==========================================================


class InterviewScheduleResource(resources.ModelResource):

    job = fields.Field(
        column_name="job",
        attribute="job",
        widget=ForeignKeyWidget(
            Job,
            "slug",
        ),
    )

    applicant = fields.Field(
        column_name="applicant",
        attribute="applicant",
        widget=ForeignKeyWidget(
            JobApplicant,
            "phone",
        ),
    )

    class Meta:

        model = InterviewSchedule

        skip_unchanged = True

        report_skipped = True

        use_bulk = True

        batch_size = 500

        import_id_fields = (
            "job",
            "applicant",
            "scheduled_datetime",
        )

        fields = (
            "id",
            "job",
            "applicant",
            "interview_type",
            "scheduled_datetime",
            "duration",
            "interviewer",
            "office_address",
            "meeting_link",
            "status",
            "feedback",
            "internal_notes",
            "whatsapp_sent",
            "reminder_sent",
            "created_at",
        )

        export_order = fields


# ==========================================================
# RESOURCE HELPERS
# ==========================================================

class BaseImportExportMixin:

    def before_import_row(self, row, **kwargs):
        """
        Hook for custom validation before import.
        """
        return row

    def after_import_row(self, row, row_result, **kwargs):
        """
        Hook after successful import.
        """
        return row_result

    def before_export(self, queryset, **kwargs):
        return queryset




# ==========================================================
# BASE RESOURCE (COMMON)
# ==========================================================

from import_export import resources


class BaseResource(resources.ModelResource):
    """
    Base Resource for all Import / Export Resources.
    """

    class Meta:
        skip_unchanged = True
        report_skipped = True
        use_bulk = True
        batch_size = 1000

    def before_import_row(self, row, **kwargs):
        return row

    def after_import_row(self, row, row_result, **kwargs):
        return row_result

    def before_export(self, queryset, **kwargs):
        return queryset

    def after_export(self, queryset, dataset, **kwargs):
        return dataset


# ==========================================================
# OFFER LETTER RESOURCE
# ==========================================================


class OfferLetterResource(BaseResource):

    applicant = fields.Field(
        column_name="applicant",
        attribute="applicant",
        widget=ForeignKeyWidget(
            JobApplicant,
            "phone",
        ),
    )

    job = fields.Field(
        column_name="job",
        attribute="job",
        widget=ForeignKeyWidget(
            Job,
            "slug",
        ),
    )

    work_location = fields.Field(
        column_name="work_location",
        attribute="work_location",
        widget=ForeignKeyWidget(
            Location,
            "name",
        ),
    )

    joining_date = fields.Field(
        column_name="joining_date",
        attribute="joining_date",
        widget=DateWidget(format="%Y-%m-%d"),
    )

    offer_date = fields.Field(
        column_name="offer_date",
        attribute="offer_date",
        widget=DateWidget(format="%Y-%m-%d"),
    )

    valid_till = fields.Field(
        column_name="valid_till",
        attribute="valid_till",
        widget=DateWidget(format="%Y-%m-%d"),
    )

    class Meta(BaseResource.Meta):

        model = OfferLetter

        import_id_fields = (
            "offer_number",
        )

        fields = (
            "id",
            "offer_number",
            "job",
            "applicant",
            "designation",
            "department",
            "joining_date",
            "probation_months",
            "annual_ctc",
            "monthly_salary",
            "reporting_manager",
            "work_location",
            "offer_date",
            "valid_till",
            "status",
            "remarks",
            "created_at",
        )

        export_order = fields


# ==========================================================
# EMPLOYEE JOINING RESOURCE
# ==========================================================


class EmployeeJoiningResource(BaseResource):

    applicant = fields.Field(
        column_name="applicant",
        attribute="applicant",
        widget=ForeignKeyWidget(
            JobApplicant,
            "phone",
        ),
    )

    offer_letter = fields.Field(
        column_name="offer_letter",
        attribute="offer_letter",
        widget=ForeignKeyWidget(
            OfferLetter,
            "offer_number",
        ),
    )

    work_location = fields.Field(
        column_name="work_location",
        attribute="work_location",
        widget=ForeignKeyWidget(
            Location,
            "name",
        ),
    )

    joining_date = fields.Field(
        column_name="joining_date",
        attribute="joining_date",
        widget=DateWidget(format="%Y-%m-%d"),
    )

    confirmation_date = fields.Field(
        column_name="confirmation_date",
        attribute="confirmation_date",
        widget=DateWidget(format="%Y-%m-%d"),
    )

    class Meta(BaseResource.Meta):

        model = EmployeeJoining

        import_id_fields = (
            "employee_code",
        )

        fields = (
            "id",
            "employee_code",
            "applicant",
            "offer_letter",
            "designation",
            "department",
            "manager",
            "work_location",
            "joining_date",
            "confirmation_date",
            "documents_verified",
            "id_card_issued",
            "welcome_mail_sent",
            "onboarding_completed",
            "status",
            "remarks",
            "created_at",
        )

        export_order = fields


# ==========================================================
# RESOURCE VALIDATIONS
# ==========================================================


class JobValidationResource(JobResource):

    def before_import_row(self, row, **kwargs):

        if not row.get("company"):
            raise ValueError("Company is required.")

        if not row.get("title"):
            raise ValueError("Job Title is required.")

        if not row.get("location"):
            raise ValueError("Location is required.")

        return row


class ApplicantValidationResource(JobApplicantResource):

    def before_import_row(self, row, **kwargs):

        if not row.get("phone"):
            raise ValueError("Phone number is required.")

        if not row.get("full_name"):
            raise ValueError("Applicant Name is required.")

        return row


class OfferValidationResource(OfferLetterResource):

    def before_import_row(self, row, **kwargs):

        if not row.get("offer_number"):
            raise ValueError("Offer Number is required.")

        return row


