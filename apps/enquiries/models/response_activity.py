from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

from .response import Response


class ResponseActivity(BaseModel):

    class ActivityType(models.TextChoices):
        CREATED = "Created", "Created"
        ASSIGNED = "Assigned", "Assigned"
        STATUS_CHANGED = "Status Changed", "Status Changed"
        FOLLOWUP = "Follow Up", "Follow Up"
        MEETING = "Meeting", "Meeting"
        NOTE = "Note", "Note"
        DOCUMENT = "Document", "Document"
        EMAIL = "Email", "Email"
        WHATSAPP = "WhatsApp", "WhatsApp"
        SMS = "SMS", "SMS"
        CALL = "Call", "Call"
        CONVERTED = "Converted", "Converted"
        CLOSED = "Closed", "Closed"

    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    activity_type = models.CharField(
        max_length=30,
        choices=ActivityType.choices,
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    activity_at = models.DateTimeField(
        auto_now_add=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="response_activities",
    )

    class Meta:
        db_table = "enquiry_response_activity"
        ordering = ["-activity_at", "-id"]
        verbose_name = "Response Activity"
        verbose_name_plural = "Response Activities"

        indexes = [
            models.Index(fields=["response"]),
            models.Index(fields=["activity_type"]),
            models.Index(fields=["activity_at"]),
        ]

    def __str__(self):
        return f"{self.response.response_no} - {self.activity_type}"