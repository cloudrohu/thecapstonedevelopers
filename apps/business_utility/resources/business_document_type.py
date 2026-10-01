from import_export import resources

from apps.business_utility.models import BusinessDocumentType


class BusinessDocumentTypeResource(resources.ModelResource):

    class Meta:

        model = BusinessDocumentType

        import_id_fields = (
            "id",
        )

        skip_unchanged = True

        report_skipped = True