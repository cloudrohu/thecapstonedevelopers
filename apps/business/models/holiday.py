from django.db import models

from apps.core.models import BaseModel

from .business import Business


class BusinessHoliday(BaseModel):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="holidays",
    )

    title = models.CharField(
        max_length=255,
    )

    holiday_date = models.DateField()

    description = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = (
            "-holiday_date",
        )

        verbose_name = "Business Holiday"

        verbose_name_plural = "Business Holidays"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "business",
                    "holiday_date",
                ],
                name="unique_business_holiday",
            ),
        ]

    def __str__(self):
        return f"{self.business} - {self.title}"