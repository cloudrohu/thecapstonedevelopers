from django.db import models

from apps.core.models import MasterBaseModel


class BusinessChain(MasterBaseModel):
    """
    Examples:
        - Domino's
        - McDonald's
        - KFC
        - Pizza Hut
        - Apollo Pharmacy
        - Reliance Trends
        - Croma
    """

    logo = models.ImageField(
        upload_to="business/chains/logos/",
        blank=True,
        null=True,
    )

    banner = models.ImageField(
        upload_to="business/chains/banners/",
        blank=True,
        null=True,
    )

    website = models.URLField(
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: fa-solid fa-store",
    )

    color = models.CharField(
        max_length=7,
        blank=True,
        help_text="Example: #0d6efd",
    )

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        ordering = (
            "display_order",
            "name",
        )

        verbose_name = "Business Chain"
        verbose_name_plural = "Business Chains"

    def __str__(self):
        return self.name