from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel
from apps.customers.models import Customer

from .enquiry_source import EnquirySource
from .enquiry_status import EnquiryStatus


class Enquiry(BaseModel):
    enquiry_no = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="enquiries",
    )

    source = models.ForeignKey(
        EnquirySource,
        on_delete=models.PROTECT,
        related_name="enquiries",
    )

    status = models.ForeignKey(
        EnquiryStatus,
        on_delete=models.PROTECT,
        related_name="enquiries",
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_enquiries",
    )

    subject = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    expected_budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
    )

    enquiry_date = models.DateField(
        default=timezone.localdate,
    )

    class Meta:
        db_table = "enquiry"
        ordering = ["-created_at"]
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"

        indexes = [
            models.Index(fields=["enquiry_no"]),
            models.Index(fields=["status"]),
            models.Index(fields=["source"]),
            models.Index(fields=["assigned_to"]),
        ]

    def save(self, *args, **kwargs):
        if not self.enquiry_no:
            last = (
                Enquiry.objects.order_by("-created_at")
                .values_list("enquiry_no", flat=True)
                .first()
            )

            if last:
                number = int(last.replace("ENQ", "")) + 1
            else:
                number = 1

            self.enquiry_no = f"ENQ{number:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.enquiry_no