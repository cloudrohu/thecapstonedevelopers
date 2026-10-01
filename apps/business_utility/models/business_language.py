from django.db import models

from apps.core.models import MasterBaseModel


class BusinessLanguage(MasterBaseModel):
    """
    Examples:
        - English
        - Hindi
        - Gujarati
        - Marathi
        - Tamil
        - Telugu
    """

    language_code = models.CharField(
        max_length=10,
        unique=True,
        help_text="ISO Language Code (Example: en, hi, gu)",
    )

    is_default = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = (
            "display_order",
            "name",
        )

        verbose_name = "Business Language"
        verbose_name_plural = "Business Languages"

    def __str__(self):
        return self.name