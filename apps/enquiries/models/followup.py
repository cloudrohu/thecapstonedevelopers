from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel

from .response import Response


class Followup(BaseModel):

    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        COMPLETED = "Completed", "Completed"
        CANCELLED = "Cancelled", "Cancelled"
        MISSED = "Missed", "Missed"

    class Type(models.TextChoices):
        CALL = "Call", "Call"
        WHATSAPP = "WhatsApp", "WhatsApp"
        EMAIL = "Email", "Email"
        SMS = "SMS", "SMS"
        VISIT = "Visit", "Visit"
        OTHER = "Other", "Other"

    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name="followups",
    )

    followup_no = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )

    followup_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.CALL,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    followup_date = models.DateTimeField()

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_followups",
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "enquiry_followup"
        ordering = ["followup_date", "-created_at"]
        verbose_name = "Follow-up"
        verbose_name_plural = "Follow-ups"

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["followup_date"]),
            models.Index(fields=["assigned_to"]),
        ]

    def save(self, *args, **kwargs):

        if not self.followup_no:
            last_id = (
                Followup.objects.order_by("-id")
                .values_list("id", flat=True)
                .first()
                or 0
            )
            self.followup_no = f"FLW{last_id + 1:06d}"

        if self.status == self.Status.COMPLETED and not self.completed_at:
            self.completed_at = timezone.now()

        if self.status != self.Status.COMPLETED:
            self.completed_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.followup_no