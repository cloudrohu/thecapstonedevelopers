from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from apps.core.models import MasterBaseModel


class BusinessCategory(MPTTModel, MasterBaseModel):
    """
    Business Category Tree

    Business
    ├── Real Estate
    │   ├── Builder
    │   ├── Real Estate Agent
    │   └── Architect
    ├── Restaurant
    ├── Hotel
    ├── Hospital
    └── School
    """

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Parent Category",
    )

    icon = models.ImageField(
        upload_to="business/categories/icons/",
        blank=True,
        null=True,
    )

    banner = models.ImageField(
        upload_to="business/categories/banners/",
        blank=True,
        null=True,
    )

    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: fa-solid fa-building",
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

    class MPTTMeta:
        order_insertion_by = [
            "display_order",
            "name",
        ]

    class Meta:
        ordering = [
            "tree_id",
            "lft",
        ]

        verbose_name = "Business Category"
        verbose_name_plural = "Business Categories"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "parent",
                    "name",
                ],
                name="unique_business_category_per_parent",
            ),
        ]

    def clean(self):

        if self.parent:

            if self.parent == self:
                raise ValidationError(
                    "Category cannot be its own parent."
                )

            if self.pk and self.parent.is_descendant_of(self):
                raise ValidationError(
                    "Category cannot be a child of its descendants."
                )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return " / ".join(
            node.name
            for node in self.get_ancestors(
                include_self=True
            )
        )