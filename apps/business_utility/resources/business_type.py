from import_export import resources

from apps.business_utility.models import BusinessType


class BusinessTypeResource(resources.ModelResource):

    class Meta:
        model = BusinessType

        import_id_fields = (
            "id",
        )

        skip_unchanged = True

        report_skipped = True