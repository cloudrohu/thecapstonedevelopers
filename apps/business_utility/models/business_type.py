from django.db import models

from apps.core.models import MasterBaseModel
from .business_category import BusinessCategory


class BusinessType(MasterBaseModel):
    """
    Example:

    Real Estate
        ├── Builder
        ├── Real Estate Agent
        ├── Architect

    Restaurant
        ├── Veg
        ├── Non Veg
        ├── Cafe
    """

    category = models.ForeignKey(
        BusinessCategory,
        on_delete=models.CASCADE,
        related_name="business_types",
    )

    icon = models.ImageField(
        upload_to="business/types/icons/",
        blank=True,
        null=True,
    )

    color = models.CharField(
        max_length=7,
        blank=True,
        help_text="Example: #0d6efd",
    )

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        ordering = [
            "display_order",
            "name",
        ]

        verbose_name = "Business Type"
        verbose_name_plural = "Business Types"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "category",
                    "name",
                ],
                name="unique_business_type_per_category",
            ),
        ]

    def __str__(self):
        return f"{self.category} → {self.name}"