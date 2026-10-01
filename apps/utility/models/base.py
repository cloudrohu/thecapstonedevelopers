from django.db import models
from django.utils.text import slugify

from apps.core.models import BaseModel


class MasterBaseModel(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=30, blank=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["display_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name