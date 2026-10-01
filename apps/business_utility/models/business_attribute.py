from django.db import models

from apps.core.models import MasterBaseModel
from .business_category import BusinessCategory


class AttributeType(models.TextChoices):

    TEXT = "TEXT", "Text"

    TEXTAREA = "TEXTAREA", "Textarea"

    NUMBER = "NUMBER", "Number"

    DECIMAL = "DECIMAL", "Decimal"

    BOOLEAN = "BOOLEAN", "Yes / No"

    DATE = "DATE", "Date"

    TIME = "TIME", "Time"

    DATETIME = "DATETIME", "Date & Time"

    EMAIL = "EMAIL", "Email"

    PHONE = "PHONE", "Phone"

    URL = "URL", "URL"

    SELECT = "SELECT", "Select"

    MULTISELECT = "MULTISELECT", "Multi Select"


class BusinessAttribute(MasterBaseModel):

    category = models.ForeignKey(
        BusinessCategory,
        on_delete=models.CASCADE,
        related_name="attributes",
    )

    attribute_type = models.CharField(
        max_length=20,
        choices=AttributeType.choices,
        default=AttributeType.TEXT,
    )

    placeholder = models.CharField(
        max_length=255,
        blank=True,
    )

    default_value = models.CharField(
        max_length=255,
        blank=True,
    )

    help_text = models.CharField(
        max_length=255,
        blank=True,
    )

    is_required = models.BooleanField(
        default=False,
    )

    is_filterable = models.BooleanField(
        default=False,
    )

    is_searchable = models.BooleanField(
        default=False,
    )

    class Meta:

        ordering = (
            "display_order",
            "name",
        )

        verbose_name = "Business Attribute"

        verbose_name_plural = "Business Attributes"

        constraints = [

            models.UniqueConstraint(

                fields=[

                    "category",
                    "name",

                ],

                name="unique_business_attribute",

            ),

        ]

    def __str__(self):

        return f"{self.category} → {self.name}"