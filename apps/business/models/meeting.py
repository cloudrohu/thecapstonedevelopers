from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

from .enquiry import BusinessEnquiry


class MeetingType(models.TextChoices):

    OFFICE = "OFFICE", "Office Meeting"

    SITE_VISIT = "SITE_VISIT", "Site Visit"

    ONLINE = "ONLINE", "Online Meeting"

    PHONE = "PHONE", "Phone Meeting"

    OTHER = "OTHER", "Other"


class MeetingStatus(models.TextChoices):

    SCHEDULED = "SCHEDULED", "Scheduled"

    COMPLETED = "COMPLETED", "Completed"

    CANCELLED = "CANCELLED", "Cancelled"

    RESCHEDULED = "RESCHEDULED", "Rescheduled"


class BusinessMeeting(BaseModel):

    enquiry = models.ForeignKey(
        BusinessEnquiry,
        on_delete=models.CASCADE,
        related_name="meetings",
    )

    meeting_type = models.CharField(
        max_length=20,
        choices=MeetingType.choices,
        default=MeetingType.OFFICE,
    )

    meeting_date = models.DateField()

    meeting_time = models.TimeField(
        blank=True,
        null=True,
    )

    meeting_location = models.CharField(
        max_length=255,
        blank=True,
    )

    agenda = models.TextField(
        blank=True,
    )

    outcome = models.TextField(
        blank=True,
    )

    next_action = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=MeetingStatus.choices,
        default=MeetingStatus.SCHEDULED,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="business_meetings",
    )

    class Meta:

        ordering = (
            "-meeting_date",
            "-meeting_time",
        )

        verbose_name = "Business Meeting"

        verbose_name_plural = "Business Meetings"

    def __str__(self):
        return (
            f"{self.enquiry.customer_name} "
            f"- {self.meeting_date}"
        )