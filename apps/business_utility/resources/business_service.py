from import_export import resources

from apps.business_utility.models import BusinessService


class BusinessServiceResource(resources.ModelResource):

    class Meta:

        model = BusinessService

        import_id_fields = (
            "id",
        )

        skip_unchanged = True

        report_skipped = True