from django.db import models
from django.conf import settings

from apps.core.models import BaseModel
from apps.properties.models import Project


class ImportStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    RUNNING = "Running", "Running"
    COMPLETED = "Completed", "Completed"
    FAILED = "Failed", "Failed"


class WebsiteType(models.TextChoices):
    ACRES99 = "99acres", "99acres"
    MAGICBRICKS = "MagicBricks", "MagicBricks"
    HOUSING = "Housing", "Housing"
    NOBROKER = "NoBroker", "NoBroker"
    DEVELOPER = "Developer", "Developer"


class ImportProject(BaseModel):

    url = models.URLField()

    website = models.CharField(
        max_length=30,
        choices=WebsiteType.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=ImportStatus.choices,
        default=ImportStatus.PENDING,
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    log = models.TextField(
        blank=True,
    )

    error = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return self.url