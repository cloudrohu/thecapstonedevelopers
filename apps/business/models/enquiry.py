from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

from .business import Business


class EnquirySource(models.TextChoices):

    WEBSITE = "WEBSITE", "Website"
    GOOGLE = "GOOGLE", "Google"
    FACEBOOK = "FACEBOOK", "Facebook"
    INSTAGRAM = "INSTAGRAM", "Instagram"
    WHATSAPP = "WHATSAPP", "WhatsApp"
    CALL = "CALL", "Call"
    WALK_IN = "WALK_IN", "Walk In"
    REFERRAL = "REFERRAL", "Referral"
    OTHER = "OTHER", "Other"


class EnquiryStatus(models.TextChoices):

    NEW = "NEW", "New"
    CONTACTED = "CONTACTED", "Contacted"
    QUALIFIED = "QUALIFIED", "Qualified"
    CONVERTED = "CONVERTED", "Converted"
    LOST = "LOST", "Lost"


class EnquiryPriority(models.TextChoices):

    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    URGENT = "URGENT", "Urgent"


class BusinessEnquiry(BaseModel):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="enquiries",
    )

    customer_name = models.CharField(
        max_length=255,
    )

    company_name = models.CharField(
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

    source = models.CharField(
        max_length=20,
        choices=EnquirySource.choices,
        default=EnquirySource.WEBSITE,
    )

    priority = models.CharField(
        max_length=10,
        choices=EnquiryPriority.choices,
        default=EnquiryPriority.MEDIUM,
    )

    status = models.CharField(
        max_length=20,
        choices=EnquiryStatus.choices,
        default=EnquiryStatus.NEW,
    )

    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    requirement = models.TextField(
        blank=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="business_enquiries",
    )

    expected_close_date = models.DateField(
        blank=True,
        null=True,
    )

    class Meta:

        ordering = (
            "-created_at",
        )

        verbose_name = "Business Enquiry"

        verbose_name_plural = "Business Enquiries"

    def __str__(self):
        return f"{self.customer_name} → {self.business}"