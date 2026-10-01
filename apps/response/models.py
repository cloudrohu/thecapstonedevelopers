import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from apps.companies.models import CompanyCategory
from apps.core.models import BaseModel
from apps.utility.models import (
    Location,
    LocationType,
    PostalCode,
    RequirementType,
)


def clean_phone_last10(phone: str):
    if not phone:
        return None
    phone = str(phone).strip()
    digits = re.sub(r"\D", "", phone)
    if len(digits) >= 10:
        return digits[-10:]
    return digits


class Response(BaseModel):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Meeting", "Meeting"),
        ("Follow_Up", "Follow Up"),
        ("Meeting_FollowUp", "Meeting / Follow Up"),
        ("Not_received", "Not Received"),
        ("Software_company", "Software Company"),
        ("For_job", "For Job"),
        ("Training", "Training"),
        ("Fake_lead", "Fake Lead"),
        ("Deal_close", "Deal Close"),
    ]

    LEAD_SOURCE_CHOICES = [
        ("instagram", "Instagram Ads"),
        ("facebook", "Facebook Ads"),
        ("google", "Google Ads"),
        ("website", "Website"),
        ("whatsapp", "WhatsApp"),
        ("Just Dial", "Just Dial"),
        ("manual", "Manual"),
    ]

    lead_source = models.CharField(
        max_length=20,
        choices=LEAD_SOURCE_CHOICES,
        default="manual",
        db_index=True,
    )
    whatsapp_welcome_sent = models.BooleanField(default=False)
    whatsapp_followup_1_sent = models.BooleanField(default=False)
    whatsapp_followup_2_sent = models.BooleanField(default=False)

    is_converted = models.BooleanField(default=False)
    converted_at = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=25, choices=STATUS_CHOICES, default="New", db_index=True
    )
    response_no = models.CharField(
        max_length=10, unique=True, editable=False
    )
    contact_no = models.CharField(
        max_length=16, unique=True, null=True, blank=True, db_index=True
    )
    contact_persone = models.CharField(max_length=500, blank=True, null=True)
    business_name = models.CharField(max_length=500, blank=True, null=True)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_response",
    )
    business_category = models.ForeignKey(
        CompanyCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    requirement_types = models.ManyToManyField(
        RequirementType, blank=True, related_name="responses"
    )

    city = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="response_city",
        limit_choices_to={"location_type": LocationType.DISTRICT_CITY},
        null=True,
        blank=True,
    )
    locality = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="response_locality",
        limit_choices_to={"location_type": LocationType.LOCALITY_AREA},
        null=True,
        blank=True,
    )
    area = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="response_area",
        limit_choices_to={"location_type": LocationType.SUBLOCALITY_AREA},
        null=True,
        blank=True,
    )
    postal_code = models.ForeignKey(
        PostalCode,
        on_delete=models.PROTECT,
        related_name="response",
        null=True,
        blank=True,
    )
    address = models.TextField(blank=True)

    def refresh_status(self):
        has_meeting = Meeting.objects.filter(response=self).exists()
        has_followup = Followup.objects.filter(response=self).exists()

        if has_meeting and has_followup:
            status = "Meeting_FollowUp"
        elif has_meeting:
            status = "Meeting"
        elif has_followup:
            status = "Follow_Up"
        else:
            status = "New"

        if self.status != status:
            self.status = status
            self.save(update_fields=["status"])

    def clean(self):
        if self.locality and self.city and self.locality.parent_id != self.city_id:
            raise ValidationError({"locality": "Selected locality does not belong to selected city."})
        if self.area and self.locality and self.area.parent_id != self.locality_id:
            raise ValidationError({"area": "Selected area does not belong to selected locality."})

    def save(self, *args, **kwargs):
        if self.contact_no:
            self.contact_no = clean_phone_last10(self.contact_no)

        if not self.response_no:
            with transaction.atomic():
                last = Response.objects.select_for_update().order_by("-response_no").first()
                number = int(last.response_no[1:]) + 1 if (last and last.response_no) else 1
                self.response_no = f"R{number:06d}"

        if self.is_converted and not self.converted_at:
            self.converted_at = timezone.now()
        elif not self.is_converted:
            self.converted_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.response_no} - {self.contact_no or 'No Number'}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Response"
        verbose_name_plural = "0. Responses"
        indexes = [
            models.Index(fields=["response_no"]),
            models.Index(fields=["contact_no"]),
            models.Index(fields=["status"]),
            models.Index(fields=["lead_source"]),
            models.Index(fields=["is_converted"]),
        ]


class Meeting(BaseModel):
    MEETING_STATUS_CHOICES = [
        ("New Meeting", "New Meeting"),
        ("Re Meeting", "Re Meeting"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    response = models.OneToOneField(Response, on_delete=models.CASCADE, related_name="meeting")
    meeting_no = models.CharField(max_length=10, unique=True, editable=False)
    status = models.CharField(max_length=25, choices=MEETING_STATUS_CHOICES, default="New Meeting")
    meeting_date = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_response_meetings")
    comment = models.CharField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.meeting_no:
            with transaction.atomic():
                last = Meeting.objects.select_for_update().order_by("-meeting_no").first()
                number = int(last.meeting_no[2:]) + 1 if (last and last.meeting_no) else 1
                self.meeting_no = f"RM{number:06d}"

        super().save(*args, **kwargs)
        self.response.refresh_status()

        if self.status == "Deal Done":
            Response.objects.filter(pk=self.response_id).update(
                status="Deal_close",
                is_converted=True,
                converted_at=timezone.now(),
            )

    def delete(self, *args, **kwargs):
        resp = self.response
        super().delete(*args, **kwargs)
        resp.refresh_status()

    def __str__(self):
        return f"{self.meeting_no} - {self.status}"

    class Meta:
        ordering = ("-meeting_date",)
        verbose_name = "Meeting"
        verbose_name_plural = "1. Meetings"


class Followup(BaseModel):
    FOLLOWUP_STATUS_CHOICES = [
        ("New Followup", "New Followup"),
        ("Re Followup", "Re Followup"),
        ("Cancelled", "Cancelled"),
        ("Deal Done", "Deal Done"),
    ]

    response = models.OneToOneField(Response, on_delete=models.CASCADE, related_name="followup")
    followup_no = models.CharField(max_length=10, unique=True, editable=False)
    status = models.CharField(max_length=25, choices=FOLLOWUP_STATUS_CHOICES, default="New Followup")
    followup_date = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_response_followups")
    comment = models.CharField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.followup_no:
            with transaction.atomic():
                last = Followup.objects.select_for_update().order_by("-followup_no").first()
                number = int(last.followup_no[2:]) + 1 if (last and last.followup_no) else 1
                self.followup_no = f"RF{number:06d}"

        super().save(*args, **kwargs)
        self.response.refresh_status()

        if self.status == "Deal Done":
            Response.objects.filter(pk=self.response_id).update(
                status="Deal_close",
                is_converted=True,
                converted_at=timezone.now(),
            )

    def delete(self, *args, **kwargs):
        resp = self.response
        super().delete(*args, **kwargs)
        resp.refresh_status()

    def __str__(self):
        return f"{self.followup_no} - {self.status}"

    class Meta:
        ordering = ("-followup_date",)
        verbose_name = "Follow Up"
        verbose_name_plural = "2. Follow Ups"


class Comment(BaseModel):
    response = models.ForeignKey(Response, blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Comment {self.id} - {self.comment[:25] if self.comment else ''}"


class VoiceRecording(BaseModel):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="recordings")
    file = models.FileField(upload_to="voice_recordings/")
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Recording {self.id} - {self.file.name}"