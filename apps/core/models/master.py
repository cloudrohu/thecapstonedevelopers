from django.db import models
from django.utils.text import slugify

from .base import BaseModel


class MasterBaseModel(BaseModel):

    name = models.CharField(
        max_length=255,
        db_index=True,
    )

    code = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    description = models.TextField(
        blank=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if self.name and not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)