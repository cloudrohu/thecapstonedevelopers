from django.db import models

from apps.core.models import BaseModel
from apps.utility.models import Location

from apps.business_utility.models import (
    BusinessCategory,
    BusinessType,
    BusinessChain,
    BusinessAmenity,
    BusinessService,
    BusinessTag,
    BusinessLanguage,
    BusinessPaymentMethod,
)


class Business(BaseModel):

    # ==========================================
    # Basic Information
    # ==========================================

    category = models.ForeignKey(
        BusinessCategory,
        on_delete=models.PROTECT,
        related_name="businesses",
    )

    business_type = models.ForeignKey(
        BusinessType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="businesses",
    )

    chain = models.ForeignKey(
        BusinessChain,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="businesses",
    )

    name = models.CharField(
        max_length=255,
        db_index=True,
    )

    code = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
    )

    slug = models.SlugField(
        unique=True,
        db_index=True,
    )

    short_description = models.CharField(
        max_length=500,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    # ==========================================
    # Contact
    # ==========================================

    owner_name = models.CharField(
        max_length=255,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
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

    # ==========================================
    # Address
    # ==========================================

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="businesses",
    )

    address = models.TextField()

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )

    # ==========================================
    # Media
    # ==========================================

    logo = models.ImageField(
        upload_to="business/logo/",
        blank=True,
        null=True,
    )

    cover_image = models.ImageField(
        upload_to="business/cover/",
        blank=True,
        null=True,
    )

    # ==========================================
    # Business Information
    # ==========================================

    gst_number = models.CharField(
        max_length=20,
        blank=True,
    )

    pan_number = models.CharField(
        max_length=10,
        blank=True,
    )

    established_year = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    employee_count = models.PositiveIntegerField(
        default=0,
    )

    # ==========================================
    # Features
    # ==========================================

    amenities = models.ManyToManyField(
        BusinessAmenity,
        blank=True,
        related_name="businesses",
    )

    services = models.ManyToManyField(
        BusinessService,
        blank=True,
        related_name="businesses",
    )

    tags = models.ManyToManyField(
        BusinessTag,
        blank=True,
        related_name="businesses",
    )

    payment_methods = models.ManyToManyField(
        BusinessPaymentMethod,
        blank=True,
        related_name="businesses",
    )

    languages = models.ManyToManyField(
        BusinessLanguage,
        blank=True,
        related_name="businesses",
    )

    # ==========================================
    # Status
    # ==========================================

    is_verified = models.BooleanField(
        default=False,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    is_premium = models.BooleanField(
        default=False,
    )

    # ==========================================
    # Statistics
    # ==========================================

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
    )

    review_count = models.PositiveIntegerField(
        default=0,
    )

    view_count = models.PositiveIntegerField(
        default=0,
    )

    class Meta:

        ordering = (
            "name",
        )

        verbose_name = "Business"

        verbose_name_plural = "Businesses"

    def __str__(self):
        return self.name