from django.db import models

from apps.core.models import MasterBaseModel
from .business_category import BusinessCategory


class BusinessDocumentType(MasterBaseModel):

    category = models.ForeignKey(
        BusinessCategory,
        on_delete=models.CASCADE,
        related_name="document_types",
        null=True,
        blank=True,
        help_text="Leave blank for common documents.",
    )

    is_mandatory = models.BooleanField(
        default=False,
        help_text="Required for business verification.",
    )

    class Meta:
        ordering = (
            "display_order",
            "name",
        )

        verbose_name = "Business Document Type"
        verbose_name_plural = "Business Document Types"

        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_business_document_type_per_category",
            ),
        ]

    def __str__(self):
        if self.category:
            return f"{self.category} → {self.name}"
        return self.name