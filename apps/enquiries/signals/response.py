from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.enquiries.models import (
    Response,
    ResponseActivity,
)


@receiver(post_save, sender=Response)
def create_response_activity(sender, instance, created, **kwargs):
    if created:
        ResponseActivity.objects.create(
            response=instance,
            activity_type=ResponseActivity.ActivityType.CREATED,
            title="Response Created",
            description="Response was created automatically.",
            created_by=instance.assigned_to,
        )