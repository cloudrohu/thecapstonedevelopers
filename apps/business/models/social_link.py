from django.db import models

from apps.core.models import BaseModel

from .business import Business


class SocialPlatform(models.TextChoices):

    WEBSITE = "WEBSITE", "Website"

    FACEBOOK = "FACEBOOK", "Facebook"

    INSTAGRAM = "INSTAGRAM", "Instagram"

    X = "X", "X (Twitter)"

    LINKEDIN = "LINKEDIN", "LinkedIn"

    YOUTUBE = "YOUTUBE", "YouTube"

    WHATSAPP = "WHATSAPP", "WhatsApp"

    TELEGRAM = "TELEGRAM", "Telegram"

    PINTEREST = "PINTEREST", "Pinterest"

    SNAPCHAT = "SNAPCHAT", "Snapchat"

    TIKTOK = "TIKTOK", "TikTok"

    OTHER = "OTHER", "Other"


class BusinessSocialLink(BaseModel):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="social_links",
    )

    platform = models.CharField(
        max_length=20,
        choices=SocialPlatform.choices,
    )

    url = models.URLField()

    username = models.CharField(
        max_length=255,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    class Meta:

        ordering = (
            "platform",
        )

        verbose_name = "Business Social Link"

        verbose_name_plural = "Business Social Links"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "business",
                    "platform",
                ],
                name="unique_business_social_platform",
            ),
        ]

    def __str__(self):
        return f"{self.business} - {self.get_platform_display()}"