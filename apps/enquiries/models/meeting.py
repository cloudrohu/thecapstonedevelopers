from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel

from .response import Response


class Meeting(BaseModel):

    class MeetingType(models.TextChoices):
        OFFICE = "Office", "Office"
        SITE_VISIT = "Site Visit", "Site Visit"
        CLIENT_PLACE = "Client Place", "Client Place"
        ONLINE = "Online", "Online"
        PHONE = "Phone", "Phone"

    class Status(models.TextChoices):
        SCHEDULED = "Scheduled", "Scheduled"
        COMPLETED = "Completed", "Completed"
        CANCELLED = "Cancelled", "Cancelled"
        RESCHEDULED = "Rescheduled", "Rescheduled"
        NO_SHOW = "No Show", "No Show"

    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name="meetings",
    )

    meeting_no = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )

    meeting_type = models.CharField(
        max_length=20,
        choices=MeetingType.choices,
        default=MeetingType.OFFICE,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )

    meeting_date = models.DateTimeField()

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_meetings",
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "enquiry_meeting"
        ordering = ["meeting_date", "-created_at"]
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["meeting_date"]),
            models.Index(fields=["assigned_to"]),
        ]

    def save(self, *args, **kwargs):

        if not self.meeting_no:
            last_id = (
                Meeting.objects.order_by("-id")
                .values_list("id", flat=True)
                .first()
                or 0
            )
            self.meeting_no = f"MTG{last_id + 1:06d}"

        if self.status == self.Status.COMPLETED and not self.completed_at:
            self.completed_at = timezone.now()

        if self.status != self.Status.COMPLETED:
            self.completed_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.meeting_no