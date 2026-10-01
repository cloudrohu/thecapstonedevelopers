from import_export import resources

from apps.business_utility.models import BusinessChain


class BusinessChainResource(resources.ModelResource):

    class Meta:

        model = BusinessChain

        import_id_fields = (
            "id",
        )

        skip_unchanged = True

        report_skipped = True