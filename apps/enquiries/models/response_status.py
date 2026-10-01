from django.db import models

from apps.core.models import BaseModel


class ResponseStatus(BaseModel):
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
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    is_default = models.BooleanField(
        default=False,
    )

    is_closed = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "enquiry_status"
        ordering = ["sort_order", "name"]
        verbose_name = "Enquiry Status"
        verbose_name_plural = "Enquiry Statuses"

    def __str__(self):
        return self.name