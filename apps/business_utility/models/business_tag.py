from django.db import models

from apps.core.models import MasterBaseModel
from .business_category import BusinessCategory


class BusinessTag(MasterBaseModel):

    category = models.ForeignKey(
        BusinessCategory,
        on_delete=models.CASCADE,
        related_name="tags",
    )

    color = models.CharField(
        max_length=7,
        blank=True,
        help_text="Example: #198754",
    )

    class Meta:
        ordering = (
            "display_order",
            "name",
        )

        verbose_name = "Business Tag"
        verbose_name_plural = "Business Tags"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "category",
                    "name",
                ],
                name="unique_business_tag_per_category",
            ),
        ]

    def __str__(self):
        return f"{self.category} → {self.name}"