from django.db import models

from apps.core.models import MasterBaseModel
from .business_category import BusinessCategory


class BusinessAmenity(MasterBaseModel):

    category = models.ForeignKey(
        BusinessCategory,
        on_delete=models.CASCADE,
        related_name="amenities",
    )

    icon = models.ImageField(
        upload_to="business/amenities/icons/",
        blank=True,
        null=True,
    )

    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: fa-solid fa-wifi",
    )

    color = models.CharField(
        max_length=7,
        blank=True,
        help_text="Example: #198754",
    )

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        ordering = (
            "display_order",
            "name",
        )

        verbose_name = "Business Amenity"
        verbose_name_plural = "Business Amenities"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "category",
                    "name",
                ],
                name="unique_business_amenity_per_category",
            ),
        ]

    def __str__(self):
        return f"{self.category} → {self.name}"