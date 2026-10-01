from django.db import models

from apps.core.models import BaseModel

from apps.business_utility.models import (
    BusinessAttribute,
)

from .business import Business


class BusinessAttributeValue(BaseModel):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="attribute_values",
    )

    attribute = models.ForeignKey(
        BusinessAttribute,
        on_delete=models.CASCADE,
        related_name="values",
    )

    value = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = (
            "attribute__display_order",
            "attribute__name",
        )

        verbose_name = "Business Attribute Value"

        verbose_name_plural = "Business Attribute Values"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "business",
                    "attribute",
                ],
                name="unique_business_attribute_value",
            ),
        ]

    def __str__(self):
        return (
            f"{self.business} → "
            f"{self.attribute.name}"
        )