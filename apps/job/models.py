from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from apps.core.models import BaseModel
from apps.companies.models import Company
from apps.utility.models import Location, PostalCode, LocationType
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


class JobType(models.TextChoices):
    FULL_TIME = "FULL_TIME", "Full Time"
    PART_TIME = "PART_TIME", "Part Time"
    CONTRACT = "CONTRACT", "Contract"
    INTERNSHIP = "INTERNSHIP", "Internship"
    FREELANCE = "FREELANCE", "Freelance"


class WorkMode(models.TextChoices):
    OFFICE = "OFFICE", "Office"
    REMOTE = "REMOTE", "Remote"
    HYBRID = "HYBRID", "Hybrid"
    FIELD = "FIELD", "Field"


class Gender(models.TextChoices):
    ANY = "ANY", "Any"
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"


class JobStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    PAUSED = "PAUSED", "Paused"
    CLOSED = "CLOSED", "Closed"
    EXPIRED = "EXPIRED", "Expired"


class Job(BaseModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="jobs",
    )

    title = models.ForeignKey(
        JobTitle,
        on_delete=models.PROTECT,
        related_name="jobs",
    )

    category = models.ForeignKey(
        JobCategory,
        on_delete=models.PROTECT,
        related_name="jobs",
    )

    industry = models.ForeignKey(
        JobIndustry,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="jobs",
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="jobs",
        limit_choices_to={
            "location_type__in": [
                LocationType.LOCALITY_AREA,
                LocationType.SUBLOCALITY_AREA,
            ]
        },
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="jobs",
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )

    vacancy = models.PositiveIntegerField(default=1)

    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices,
    )

    work_mode = models.CharField(
        max_length=20,
        choices=WorkMode.choices,
        default=WorkMode.OFFICE,
    )

    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        default=Gender.ANY,
    )

    minimum_age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    maximum_age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    minimum_experience = models.PositiveIntegerField(
        default=0,
        help_text="Experience in Months",
    )

    maximum_experience = models.PositiveIntegerField(
        default=0,
        help_text="Experience in Months",
    )

    qualification = models.CharField(
        max_length=255,
        blank=True,
    )

    salary_type = models.ForeignKey(
        SalaryType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    minimum_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    maximum_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    negotiable = models.BooleanField(default=False)

    hide_salary = models.BooleanField(default=False)

    working_days = models.ForeignKey(
        WorkingDaysOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    timing = models.ForeignKey(
        JobTimingTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    skills = models.ManyToManyField(
        JobSkill,
        blank=True,
        related_name="jobs",
    )

    benefits = models.ManyToManyField(
        JobBenefit,
        blank=True,
        related_name="jobs",
    )

    assets = models.ManyToManyField(
        JobAsset,
        blank=True,
        related_name="jobs",
    )

    documents = models.ManyToManyField(
        JobDocument,
        blank=True,
        related_name="jobs",
    )

    languages = models.ManyToManyField(
        JobLanguageRequirement,
        blank=True,
        related_name="jobs",
    )

    short_description = models.TextField(blank=True)

    description = CKEditor5Field(
        blank=True,
        null=True,
    )

    responsibilities = CKEditor5Field(
        blank=True,
        null=True,
    )

    requirements = CKEditor5Field(
        blank=True,
        null=True,
    )

    featured = models.BooleanField(default=False)

    published = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.DRAFT,
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
    )

    meta_title = models.CharField(
        max_length=255,
        blank=True,
    )

    meta_description = models.TextField(blank=True)

    meta_keywords = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["title"]),
            models.Index(fields=["category"]),
            models.Index(fields=["status"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["published"]),
            models.Index(fields=["location"]),
        ]

    def clean(self):

        if (
            self.maximum_salary
            and self.minimum_salary
            and self.maximum_salary < self.minimum_salary
        ):
            raise ValidationError(
                "Maximum salary cannot be less than minimum salary."
            )

        if (
            self.maximum_experience
            and self.minimum_experience
            and self.maximum_experience < self.minimum_experience
        ):
            raise ValidationError(
                "Maximum experience cannot be less than minimum experience."
            )

        if self.postal_code and self.location:
            if self.postal_code.location_id != self.location_id:
                raise ValidationError(
                    {
                        "postal_code": "Selected postal code does not belong to selected location."
                    }
                )

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(
                f"{self.company.name}-{self.title.name}-{self.location.name}"
            )

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.company}"




# ==========================================================
# JOB APPLICANT
# ==========================================================

from django.utils import timezone


class ApplicationStatus(models.TextChoices):
    APPLIED = "APPLIED", "Applied"
    SHORTLISTED = "SHORTLISTED", "Shortlisted"
    INTERVIEW = "INTERVIEW", "Interview"
    SELECTED = "SELECTED", "Selected"
    REJECTED = "REJECTED", "Rejected"
    HOLD = "HOLD", "On Hold"
    JOINED = "JOINED", "Joined"


class ApplySource(models.TextChoices):
    WEBSITE = "WEBSITE", "Website"
    ADMIN = "ADMIN", "Admin"
    APNA = "APNA", "Apna"
    JOBHAI = "JOBHAI", "Job Hai"
    INDEED = "INDEED", "Indeed"
    WORKINDIA = "WORKINDIA", "Work India"
    WHATSAPP = "WHATSAPP", "WhatsApp"
    CALL = "CALL", "Call"
    IMPORT = "IMPORT", "Imported"


class NoticePeriod(models.TextChoices):
    IMMEDIATE = "IMMEDIATE", "Immediate"
    DAYS_15 = "15_DAYS", "15 Days"
    DAYS_30 = "30_DAYS", "30 Days"
    DAYS_45 = "45_DAYS", "45 Days"
    DAYS_60 = "60_DAYS", "60 Days"


class JobApplicant(BaseModel):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applicants",
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="job_applicants",
        limit_choices_to={
            "location_type__in": [
                LocationType.LOCALITY_AREA,
                LocationType.SUBLOCALITY_AREA,
            ]
        },
        null=True,
        blank=True,
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="job_applicants",
    )

    full_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=15)

    alternate_phone = models.CharField(
        max_length=15,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="jobs/applicants/images/",
        blank=True,
        null=True,
    )

    resume = models.FileField(
        upload_to="jobs/applicants/resume/",
        blank=True,
        null=True,
    )

    current_company = models.CharField(
        max_length=200,
        blank=True,
    )

    current_designation = models.CharField(
        max_length=200,
        blank=True,
    )

    experience = models.PositiveIntegerField(
        default=0,
        help_text="Experience in Months",
    )

    current_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    expected_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    notice_period = models.CharField(
        max_length=20,
        choices=NoticePeriod.choices,
        blank=True,
    )

    expected_joining_date = models.DateField(
        blank=True,
        null=True,
    )

    cover_letter = CKEditor5Field(
        blank=True,
        null=True,
    )

    remarks = models.TextField(blank=True)

    source = models.CharField(
        max_length=20,
        choices=ApplySource.choices,
        default=ApplySource.WEBSITE,
    )

    allow_whatsapp = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED,
    )

    applied_at = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        ordering = ["-applied_at"]
        verbose_name = "Job Applicant"
        verbose_name_plural = "Job Applicants"

        indexes = [
            models.Index(fields=["phone"]),
            models.Index(fields=["status"]),
            models.Index(fields=["job"]),
            models.Index(fields=["location"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["job", "phone"],
                name="unique_job_phone",
            )
        ]

    def clean(self):

        if self.postal_code and self.location:
            if self.postal_code.location_id != self.location_id:
                raise ValidationError(
                    "Postal code does not belong to selected location."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.phone})"


# ==========================================================
# INTERVIEW SCHEDULE
# ==========================================================


class InterviewType(models.TextChoices):
    HR = "HR", "HR Round"
    TECHNICAL = "TECHNICAL", "Technical Round"
    FINAL = "FINAL", "Final Round"
    VIDEO = "VIDEO", "Video Call"
    TELEPHONIC = "TELEPHONIC", "Telephonic"
    FACE_TO_FACE = "FACE_TO_FACE", "Face To Face"


class InterviewStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    CONFIRMED = "CONFIRMED", "Confirmed"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"
    RESCHEDULED = "RESCHEDULED", "Rescheduled"
    NO_SHOW = "NO_SHOW", "No Show"


class InterviewSchedule(BaseModel):

    applicant = models.ForeignKey(
        JobApplicant,
        on_delete=models.CASCADE,
        related_name="interviews",
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="interviews",
    )

    interview_type = models.CharField(
        max_length=20,
        choices=InterviewType.choices,
    )

    scheduled_datetime = models.DateTimeField()

    duration = models.PositiveIntegerField(default=30)

    interviewer = models.CharField(
        max_length=200,
        blank=True,
    )

    meeting_link = models.URLField(blank=True)

    office_address = models.CharField(
        max_length=300,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=InterviewStatus.choices,
        default=InterviewStatus.SCHEDULED,
    )

    feedback = CKEditor5Field(
        blank=True,
        null=True,
    )

    internal_notes = models.TextField(blank=True)

    whatsapp_sent = models.BooleanField(default=False)

    reminder_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["scheduled_datetime"]

        indexes = [
            models.Index(fields=["scheduled_datetime"]),
            models.Index(fields=["status"]),
        ]

    def save(self, *args, **kwargs):

        if not self.job_id:
            self.job = self.applicant.job

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.applicant.full_name} - "
            f"{self.get_interview_type_display()}"
        )


# ==========================================================
# OFFER LETTER
# ==========================================================


class OfferStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    GENERATED = "GENERATED", "Generated"
    SENT = "SENT", "Sent"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"
    EXPIRED = "EXPIRED", "Expired"
    CANCELLED = "CANCELLED", "Cancelled"


class OfferLetter(BaseModel):

    applicant = models.OneToOneField(
        JobApplicant,
        on_delete=models.CASCADE,
        related_name="offer_letter",
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="offer_letters",
    )

    offer_number = models.CharField(
        max_length=50,
        unique=True,
    )

    designation = models.CharField(
        max_length=200,
    )

    department = models.CharField(
        max_length=200,
        blank=True,
    )

    joining_date = models.DateField()

    probation_months = models.PositiveIntegerField(default=6)

    annual_ctc = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    monthly_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    reporting_manager = models.CharField(
        max_length=200,
        blank=True,
    )

    work_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="offer_locations",
    )

    offer_date = models.DateField()

    valid_till = models.DateField()

    terms = CKEditor5Field(
        blank=True,
        null=True,
    )

    attachment = models.FileField(
        upload_to="jobs/offers/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=OfferStatus.choices,
        default=OfferStatus.DRAFT,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    rejected_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["-offer_date"]

        indexes = [
            models.Index(fields=["offer_number"]),
            models.Index(fields=["status"]),
        ]

    def save(self, *args, **kwargs):

        if not self.job_id:
            self.job = self.applicant.job

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.offer_number


# ==========================================================
# EMPLOYEE JOINING
# ==========================================================


class JoiningStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    DOCUMENT_PENDING = "DOCUMENT_PENDING", "Document Pending"
    JOINED = "JOINED", "Joined"
    CANCELLED = "CANCELLED", "Cancelled"


class EmployeeJoining(BaseModel):

    applicant = models.OneToOneField(
        JobApplicant,
        on_delete=models.CASCADE,
        related_name="joining",
    )

    offer_letter = models.OneToOneField(
        OfferLetter,
        on_delete=models.CASCADE,
        related_name="joining",
    )

    employee_code = models.CharField(
        max_length=30,
        unique=True,
    )

    joining_date = models.DateField()

    confirmation_date = models.DateField(
        null=True,
        blank=True,
    )

    department = models.CharField(
        max_length=200,
        blank=True,
    )

    designation = models.CharField(
        max_length=200,
    )

    manager = models.CharField(
        max_length=200,
        blank=True,
    )

    work_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="employee_locations",
    )

    documents_verified = models.BooleanField(default=False)

    id_card_issued = models.BooleanField(default=False)

    welcome_mail_sent = models.BooleanField(default=False)

    onboarding_completed = models.BooleanField(default=False)

    remarks = models.TextField(blank=True)

    status = models.CharField(
        max_length=25,
        choices=JoiningStatus.choices,
        default=JoiningStatus.PENDING,
    )

    class Meta:
        ordering = ["-joining_date"]

        indexes = [
            models.Index(fields=["employee_code"]),
            models.Index(fields=["status"]),
        ]

    def save(self, *args, **kwargs):

        if self.status == JoiningStatus.JOINED:
            self.applicant.status = ApplicationStatus.JOINED
            self.applicant.save(update_fields=["status"])

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_code} - {self.applicant.full_name}"


# ==========================================================
# JOB ACTIVITY LOG
# ==========================================================


class ActivityType(models.TextChoices):
    CREATED = "CREATED", "Job Created"
    UPDATED = "UPDATED", "Job Updated"
    APPLIED = "APPLIED", "Application Received"
    SHORTLISTED = "SHORTLISTED", "Shortlisted"
    INTERVIEW = "INTERVIEW", "Interview Scheduled"
    OFFER = "OFFER", "Offer Generated"
    JOINED = "JOINED", "Employee Joined"
    REJECTED = "REJECTED", "Rejected"


class JobActivityLog(BaseModel):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    applicant = models.ForeignKey(
        JobApplicant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="activities",
    )

    activity = models.CharField(
        max_length=30,
        choices=ActivityType.choices,
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["job"]),
            models.Index(fields=["activity"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.job} - {self.title}"