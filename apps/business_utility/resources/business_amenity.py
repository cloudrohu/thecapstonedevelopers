from import_export import resources

from apps.business_utility.models import BusinessAmenity


class BusinessAmenityResource(resources.ModelResource):

    class Meta:

        model = BusinessAmenity

        import_id_fields = (
            "id",
        )

        skip_unchanged = True

        report_skipped = True
        