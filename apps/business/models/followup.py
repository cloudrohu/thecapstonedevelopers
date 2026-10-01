from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

from .enquiry import BusinessEnquiry


class FollowUpStatus(models.TextChoices):

    PENDING = "PENDING", "Pending"

    COMPLETED = "COMPLETED", "Completed"

    CANCELLED = "CANCELLED", "Cancelled"


class FollowUpMode(models.TextChoices):

    CALL = "CALL", "Call"

    WHATSAPP = "WHATSAPP", "WhatsApp"

    EMAIL = "EMAIL", "Email"

    SMS = "SMS", "SMS"

    VISIT = "VISIT", "Visit"

    MEETING = "MEETING", "Meeting"

    OTHER = "OTHER", "Other"


class BusinessFollowUp(BaseModel):

    enquiry = models.ForeignKey(
        BusinessEnquiry,
        on_delete=models.CASCADE,
        related_name="followups",
    )

    followup_date = models.DateField()

    followup_time = models.TimeField(
        blank=True,
        null=True,
    )

    mode = models.CharField(
        max_length=20,
        choices=FollowUpMode.choices,
        default=FollowUpMode.CALL,
    )

    status = models.CharField(
        max_length=20,
        choices=FollowUpStatus.choices,
        default=FollowUpStatus.PENDING,
    )

    remarks = models.TextField(
        blank=True,
    )

    next_followup_date = models.DateField(
        blank=True,
        null=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="business_followups",
    )

    class Meta:

        ordering = (
            "-followup_date",
            "-followup_time",
        )

        verbose_name = "Business Follow Up"

        verbose_name_plural = "Business Follow Ups"

    def __str__(self):
        return (
            f"{self.enquiry.customer_name} "
            f"- {self.followup_date}"
        )