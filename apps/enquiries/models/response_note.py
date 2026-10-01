from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

from .response import Response


class ResponseNote(BaseModel):
    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    note = models.TextField()

    is_private = models.BooleanField(
        default=True,
        help_text="Visible only to internal staff.",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="response_notes",
    )

    class Meta:
        db_table = "enquiry_response_note"
        ordering = ["-created_at"]
        verbose_name = "Response Note"
        verbose_name_plural = "Response Notes"

        indexes = [
            models.Index(fields=["response"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.response.response_no} - Note #{self.pk}"