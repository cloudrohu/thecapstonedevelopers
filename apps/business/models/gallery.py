from django.db import models

from apps.core.models import BaseModel

from .business import Business


class GalleryType(models.TextChoices):

    LOGO = "LOGO", "Logo"

    COVER = "COVER", "Cover"

    IMAGE = "IMAGE", "Image"

    VIDEO = "VIDEO", "Video"

    DOCUMENT = "DOCUMENT", "Document"


class BusinessGallery(BaseModel):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="gallery",
    )

    gallery_type = models.CharField(
        max_length=20,
        choices=GalleryType.choices,
        default=GalleryType.IMAGE,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    image = models.ImageField(
        upload_to="business/gallery/images/",
        blank=True,
        null=True,
    )

    video = models.FileField(
        upload_to="business/gallery/videos/",
        blank=True,
        null=True,
    )

    document = models.FileField(
        upload_to="business/gallery/documents/",
        blank=True,
        null=True,
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    class Meta:

        ordering = (
            "display_order",
            "id",
        )

        verbose_name = "Business Gallery"

        verbose_name_plural = "Business Gallery"

    def __str__(self):
        return f"{self.business} - {self.title or self.gallery_type}"