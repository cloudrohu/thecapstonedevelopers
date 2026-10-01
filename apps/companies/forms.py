from django import forms

from apps.utility.models import (
    Location,
    PostalCode,
    LocationType,
)

from .models import Company, Branch


class LocationMixin:

    def setup_location_queryset(self):

        self.fields["locality"].queryset = Location.objects.none()
        self.fields["area"].queryset = Location.objects.none()
        self.fields["postal_code"].queryset = PostalCode.objects.none()

        # -----------------------------
        # City Selected
        # -----------------------------
        city = None

        if self.data.get("city"):
            city = self.data.get("city")

        elif self.instance.pk:
            city = self.instance.city_id

        if city:

            self.fields["locality"].queryset = Location.objects.filter(
                parent_id=city,
                location_type=LocationType.LOCALITY_AREA,
                is_active=True,
            )

        # -----------------------------
        # Locality Selected
        # -----------------------------
        locality = None

        if self.data.get("locality"):
            locality = self.data.get("locality")

        elif self.instance.pk:
            locality = self.instance.locality_id

        if locality:

            self.fields["area"].queryset = Location.objects.filter(
                parent_id=locality,
                location_type=LocationType.SUBLOCALITY_AREA,
                is_active=True,
            )

        # -----------------------------
        # Area Selected
        # -----------------------------
        area = None

        if self.data.get("area"):
            area = self.data.get("area")

        elif self.instance.pk:
            area = self.instance.area_id

        if area:

            self.fields["postal_code"].queryset = PostalCode.objects.filter(
                location_id=area,
                is_active=True,
            )

        elif locality:

            self.fields["postal_code"].queryset = PostalCode.objects.filter(
                location_id=locality,
                is_active=True,
            )


class CompanyAdminForm(LocationMixin, forms.ModelForm):

    class Meta:
        model = Company
        fields = "__all__"

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.setup_location_queryset()


class BranchAdminForm(LocationMixin, forms.ModelForm):

    class Meta:
        model = Branch
        fields = "__all__"

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.setup_location_queryset()