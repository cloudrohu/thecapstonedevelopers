from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

from .response import Response


class ResponseDocument(BaseModel):

    class DocumentType(models.TextChoices):
        IMAGE = "Image", "Image"
        PDF = "PDF", "PDF"
        DOCUMENT = "Document", "Document"
        AUDIO = "Audio", "Audio"
        VIDEO = "Video", "Video"
        SPREADSHEET = "Spreadsheet", "Spreadsheet"
        OTHER = "Other", "Other"

    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    file = models.FileField(
        upload_to="crm/response_documents/%Y/%m/",
    )

    description = models.TextField(
        blank=True,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="response_documents",
    )

    class Meta:
        db_table = "enquiry_response_document"
        ordering = ["-created_at"]
        verbose_name = "Response Document"
        verbose_name_plural = "Response Documents"

        indexes = [
            models.Index(fields=["response"]),
            models.Index(fields=["document_type"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title or self.file.name