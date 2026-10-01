from import_export import resources

from apps.business_utility.models import BusinessAttribute


class BusinessAttributeResource(resources.ModelResource):

    class Meta:

        model = BusinessAttribute

        import_id_fields = (
            "id",
        )

        skip_unchanged = True

        report_skipped = True