from django.db import models

from apps.core.models import BaseModel


class EnquirySource(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
    )

    color = models.CharField(
        max_length=30,
        default="primary",
        blank=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome icon class",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "enquiry_source"
        ordering = ["sort_order", "name"]
        verbose_name = "Enquiry Source"
        verbose_name_plural = "Enquiry Sources"

    def __str__(self):
        return self.name