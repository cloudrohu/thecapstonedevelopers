from django.db import models

from apps.core.models import BaseModel

from .business import Business


class ReviewStatus(models.TextChoices):

    PENDING = "PENDING", "Pending"

    APPROVED = "APPROVED", "Approved"

    REJECTED = "REJECTED", "Rejected"


class BusinessReview(BaseModel):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    reviewer_name = models.CharField(
        max_length=255,
    )

    reviewer_email = models.EmailField(
        blank=True,
    )

    reviewer_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    rating = models.PositiveSmallIntegerField(
        default=5,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    review = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    class Meta:

        ordering = (
            "-created_at",
        )

        verbose_name = "Business Review"

        verbose_name_plural = "Business Reviews"

    def __str__(self):
        return (
            f"{self.business} "
            f"({self.rating}/5)"
        )