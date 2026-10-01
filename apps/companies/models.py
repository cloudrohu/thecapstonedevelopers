from django.db import models

from apps.core.models import BaseModel

from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from django.conf import settings
from apps.utility.models import (
    Location,
    PostalCode,
    LocationType,
)

# ==========================================================
# COMPANY STATUS
# ==========================================================

class CompanyStatus(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    color = models.CharField(
        max_length=30,
        default="primary",
        help_text="Bootstrap color (primary, success, warning, danger...)"
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="FontAwesome icon class"
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Company Status"
        verbose_name_plural = "Company Status"

    def __str__(self):
        return self.name


# ==========================================================
# COMPANY CATEGORY
# ==========================================================

class CompanyCategory(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Company Category"
        verbose_name_plural = "Company Categories"

    def __str__(self):
        return self.name


# ==========================================================
# COMPANY INDUSTRY
# ==========================================================

class CompanyIndustry(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Company Industry"
        verbose_name_plural = "Company Industries"

    def __str__(self):
        return self.name


# ==========================================================
# COMPANY TYPE
# ==========================================================

class CompanyType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Company Type"
        verbose_name_plural = "Company Types"

    def __str__(self):
        return self.name


# ==========================================================
# COMPANY SIZE
# ==========================================================

class CompanySize(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    min_employee = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    max_employee = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["min_employee", "name"]
        verbose_name = "Company Size"
        verbose_name_plural = "Company Sizes"

    def __str__(self):
        return self.name


# ==========================================================
# GOOGLE BUSINESS STATUS
# ==========================================================

class GoogleMapStatus(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Google Map Status"
        verbose_name_plural = "Google Map Status"

    def __str__(self):
        return self.name


# ==========================================================
# DOCUMENT TYPE
# ==========================================================

class DocumentType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Document Type"
        verbose_name_plural = "Document Types"

    def __str__(self):
        return self.name




class Company(BaseModel):

    # =====================================================
    # CRM
    # =====================================================

    status = models.ForeignKey(
        CompanyStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="companies",
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_companies",
    )

    category = models.ForeignKey(
        CompanyCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="companies",
    )

    # =====================================================
    # BASIC
    # =====================================================

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    legal_name = models.CharField(
        max_length=250,
        blank=True,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )

    # =====================================================
    # CLASSIFICATION
    # =====================================================

    industry = models.ForeignKey(
        CompanyIndustry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="companies",
    )

    company_type = models.ForeignKey(
        CompanyType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="companies",
    )

    company_size = models.ForeignKey(
        CompanySize,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="companies",
    )

    # =====================================================
    # BRANDING
    # =====================================================

    logo = models.ImageField(
        upload_to="companies/logo/",
        blank=True,
        null=True,
    )

    cover_image = models.ImageField(
        upload_to="companies/cover/",
        blank=True,
        null=True,
    )

    # =====================================================
    # CONTACT
    # =====================================================

    primary_phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )

    alternate_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    whatsapp = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    # =====================================================
    # LOCATION
    # =====================================================

    city = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="companies_city",
        limit_choices_to={
            "location_type": LocationType.DISTRICT_CITY,
        },
        null=True,
        blank=True,
    )

    locality = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="companies_locality",
        null=True,
        blank=True,
        limit_choices_to={
            "location_type": LocationType.LOCALITY_AREA
        },
    )

    area = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="companies_area",
        null=True,
        blank=True,
        limit_choices_to={
            "location_type": LocationType.SUBLOCALITY_AREA
        },
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="companies",
    )

    address = models.TextField(
        blank=True,
    )

    google_map = models.URLField(
        blank=True,
    )

    # =====================================================
    # BUSINESS
    # =====================================================

    founded_year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    employee_strength = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    gst_number = models.CharField(
        max_length=20,
        blank=True,
    )

    pan_number = models.CharField(
        max_length=20,
        blank=True,
    )

    cin_number = models.CharField(
        max_length=30,
        blank=True,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )

    reviews_count = models.PositiveIntegerField(
        default=0,
    )

    google_business_status = models.ForeignKey(
        GoogleMapStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # =====================================================
    # DESCRIPTION
    # =====================================================

    short_description = models.CharField(
        max_length=300,
        blank=True,
    )

    about = CKEditor5Field(
        "About",
        config_name="default",
    )


    # =====================================================
    # SOCIAL
    # =====================================================

    facebook = models.URLField(blank=True)

    instagram = models.URLField(blank=True)

    linkedin = models.URLField(blank=True)

    twitter = models.URLField(blank=True)

    youtube = models.URLField(blank=True)

    # =====================================================
    # SEO
    # =====================================================

    meta_title = models.CharField(
        max_length=255,
        blank=True,
    )

    meta_description = models.TextField(
        blank=True,
    )

    meta_keywords = models.TextField(
        blank=True,
    )

    # =====================================================
    # FLAGS
    # =====================================================

    is_verified = models.BooleanField(
        default=False,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.primary_phone:
            self.primary_phone = (
                self.primary_phone.replace(" ", "").strip()
            )

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


# ==========================================================
# COMPANY BRANCH
# ==========================================================

class Branch(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="branches",
    )

    name = models.CharField(max_length=200)

    branch_code = models.CharField(
        max_length=50,
        blank=True,
    )

    manager_name = models.CharField(
        max_length=200,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    whatsapp = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    city = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="branch_city",
        limit_choices_to={
            "location_type": LocationType.DISTRICT_CITY
        },
        null=True,
        blank=True,
    )

    locality = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="branch_locality",
        null=True,
        blank=True,
        limit_choices_to={
            "location_type": LocationType.LOCALITY_AREA
        },
    )

    area = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="branch_area",
        null=True,
        blank=True,
        limit_choices_to={
            "location_type": LocationType.SUBLOCALITY_AREA
        },
    )

    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    address = models.TextField(blank=True)

    is_head_office = models.BooleanField(default=False)

    class Meta:
        ordering = ["company", "name"]
        unique_together = ("company", "name")

    def __str__(self):
        return f"{self.company} - {self.name}"



# ==========================================================
# DEPARTMENT
# ==========================================================

class Department(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="departments",
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    class Meta:
        ordering = ["company", "name"]
        unique_together = ("company", "name")

    def __str__(self):
        return f"{self.company} - {self.name}"


# ==========================================================
# DESIGNATION
# ==========================================================

class Designation(BaseModel):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="designations",
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    class Meta:
        ordering = ["department", "name"]
        unique_together = ("department", "name")

    def __str__(self):
        return self.name


# ==========================================================
# COMPANY CONTACT
# ==========================================================

class CompanyContact(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="contacts",
    )

    name = models.CharField(max_length=200)

    designation = models.ForeignKey(
        Designation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    email = models.EmailField(blank=True)

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    whatsapp = models.CharField(
        max_length=20,
        blank=True,
    )

    is_primary = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["company", "-is_primary", "name"]

    def __str__(self):
        return self.name


# ==========================================================
# COMPANY DOCUMENT
# ==========================================================

class CompanyDocument(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)

    file = models.FileField(
        upload_to="companies/documents/",
    )

    issue_date = models.DateField(
        null=True,
        blank=True,
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
    )

    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


# ==========================================================
# COMPANY GALLERY
# ==========================================================

class CompanyGallery(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="gallery",
    )

    image = models.ImageField(
        upload_to="companies/gallery/",
    )

    title = models.CharField(
        max_length=200,
        blank=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title or f"Image {self.pk}"