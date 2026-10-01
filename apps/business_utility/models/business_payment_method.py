from django.db import models

from apps.core.models import MasterBaseModel


class BusinessPaymentMethod(MasterBaseModel):
    """
    Examples:
        - Cash
        - UPI
        - Credit Card
        - Debit Card
        - Net Banking
        - Wallet
        - EMI
        - Cheque
    """

    icon = models.ImageField(
        upload_to="business/payment_methods/icons/",
        blank=True,
        null=True,
    )

    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: fa-solid fa-credit-card",
    )

    color = models.CharField(
        max_length=7,
        blank=True,
        help_text="Example: #198754",
    )

    is_online = models.BooleanField(
        default=False,
        help_text="Available as an online payment method.",
    )

    class Meta:
        ordering = (
            "display_order",
            "name",
        )

        verbose_name = "Business Payment Method"
        verbose_name_plural = "Business Payment Methods"

    def __str__(self):
        return self.name