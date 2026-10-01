from django.db import models

from apps.core.models import BaseModel

from apps.business_utility.models import BusinessDocumentType

from .business import Business


class VerificationStatus(models.TextChoices):

    PENDING = "PENDING", "Pending"

    APPROVED = "APPROVED", "Approved"

    REJECTED = "REJECTED", "Rejected"


class BusinessDocument(BaseModel):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_type = models.ForeignKey(
        BusinessDocumentType,
        on_delete=models.PROTECT,
        related_name="documents",
    )

    document_number = models.CharField(
        max_length=255,
        blank=True,
    )

    document = models.FileField(
        upload_to="business/documents/",
    )

    issue_date = models.DateField(
        null=True,
        blank=True,
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = (
            "document_type",
        )

        verbose_name = "Business Document"

        verbose_name_plural = "Business Documents"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "business",
                    "document_type",
                ],
                name="unique_business_document_type",
            ),
        ]

    def __str__(self):
        return (
            f"{self.business} - "
            f"{self.document_type}"
        )