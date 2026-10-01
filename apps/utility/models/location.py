from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from mptt.models import MPTTModel, TreeForeignKey

from .base import MasterBaseModel


class LocationType(models.TextChoices):
    COUNTRY = "COUNTRY", "Country"
    STATE = "STATE", "State"
    DISTRICT_CITY = "DISTRICT_CITY", "District / City"
    LOCALITY_AREA = "LOCALITY_AREA", "Locality / Area"
    SUBLOCALITY_AREA = "SUBLOCALITY_AREA", "Sub Locality / Area"


class Location(MPTTModel, MasterBaseModel):
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Parent Location",
    )

    location_type = models.CharField(
        max_length=30,
        choices=LocationType.choices,
        db_index=True,
    )

    is_top_city = models.BooleanField(
        default=False,
        help_text="Mark important cities for quick selection."
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["tree_id", "lft"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def clean(self):

        parent_rules = {
            LocationType.COUNTRY: None,
            LocationType.STATE: LocationType.COUNTRY,
            LocationType.DISTRICT_CITY: LocationType.STATE,
            LocationType.LOCALITY_AREA: LocationType.DISTRICT_CITY,
            LocationType.SUBLOCALITY_AREA: LocationType.LOCALITY_AREA,
        }

        expected_parent = parent_rules.get(self.location_type)

        if expected_parent is None:
            if self.parent:
                raise ValidationError("Country cannot have a parent.")
            return

        if not self.parent:
            raise ValidationError(
                f"{self.get_location_type_display()} must have a parent."
            )

        if self.parent.location_type != expected_parent:
            raise ValidationError(
                f"{self.get_location_type_display()} must have a "
                f"{expected_parent.replace('_', ' ').title()} parent."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return " / ".join(
            node.name
            for node in self.get_ancestors(include_self=True)
        )


class LocationAdminForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get("instance")

        if instance:
            parent_map = {
                LocationType.STATE: LocationType.COUNTRY,
                LocationType.DISTRICT_CITY: LocationType.STATE,
                LocationType.LOCALITY_AREA: LocationType.DISTRICT_CITY,
                LocationType.SUBLOCALITY_AREA: LocationType.LOCALITY_AREA,
            }

            parent_type = parent_map.get(instance.location_type)

            if parent_type:
                self.fields["parent"].queryset = Location.objects.filter(
                    location_type=parent_type
                )


class PostalCode(MasterBaseModel):
    code = models.CharField(max_length=10, unique=True)

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="postal_codes",
        limit_choices_to={
            "location_type__in": [
                LocationType.LOCALITY_AREA,
                LocationType.SUBLOCALITY_AREA,
            ]
        },
    )

    class Meta:
        ordering = ["code"]
        verbose_name = "Postal Code"
        verbose_name_plural = "Postal Codes"

    def __str__(self):
        return self.code