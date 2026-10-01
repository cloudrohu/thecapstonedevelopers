from import_export import resources

from apps.business_utility.models import BusinessTag


class BusinessTagResource(resources.ModelResource):

    class Meta:

        model = BusinessTag

        import_id_fields = (
            "id",
        )

        skip_unchanged = True

        report_skipped = True