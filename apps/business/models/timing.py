from django.db import models

from apps.core.models import BaseModel

from .business import Business


class WeekDay(models.TextChoices):

    MONDAY = "MONDAY", "Monday"
    TUESDAY = "TUESDAY", "Tuesday"
    WEDNESDAY = "WEDNESDAY", "Wednesday"
    THURSDAY = "THURSDAY", "Thursday"
    FRIDAY = "FRIDAY", "Friday"
    SATURDAY = "SATURDAY", "Saturday"
    SUNDAY = "SUNDAY", "Sunday"


class BusinessTiming(BaseModel):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="timings",
    )

    day = models.CharField(
        max_length=10,
        choices=WeekDay.choices,
    )

    opening_time = models.TimeField(
        null=True,
        blank=True,
    )

    closing_time = models.TimeField(
        null=True,
        blank=True,
    )

    is_closed = models.BooleanField(
        default=False,
    )

    is_24_hours = models.BooleanField(
        default=False,
    )

    class Meta:

        ordering = (
            "day",
        )

        verbose_name = "Business Timing"

        verbose_name_plural = "Business Timings"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "business",
                    "day",
                ],
                name="unique_business_day",
            ),
        ]

    def __str__(self):
        return f"{self.business} - {self.get_day_display()}"