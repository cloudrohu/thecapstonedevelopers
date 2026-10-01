from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel

from .enquiry import Enquiry
from .response_status import ResponseStatus


class Response(BaseModel):

    class Priority(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"
        URGENT = "Urgent", "Urgent"

    enquiry = models.OneToOneField(
        Enquiry,
        on_delete=models.CASCADE,
        related_name="response",
    )

    response_no = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )

    status = models.ForeignKey(
        ResponseStatus,
        on_delete=models.PROTECT,
        related_name="responses",
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_responses",
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    first_response_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    last_activity_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    next_followup_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_converted = models.BooleanField(
        default=False,
    )

    converted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "enquiry_response"
        ordering = ["-created_at"]
        verbose_name = "Response"
        verbose_name_plural = "Responses"

        indexes = [
            models.Index(fields=["response_no"]),
            models.Index(fields=["status"]),
            models.Index(fields=["assigned_to"]),
            models.Index(fields=["is_converted"]),
            models.Index(fields=["next_followup_at"]),
        ]

    def save(self, *args, **kwargs):

        if not self.response_no:
            last_id = (
                Response.objects.order_by("-id")
                .values_list("id", flat=True)
                .first()
                or 0
            )
            self.response_no = f"RSP{last_id + 1:06d}"

        if self.is_converted:
            if not self.converted_at:
                self.converted_at = timezone.now()
        else:
            self.converted_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.response_no