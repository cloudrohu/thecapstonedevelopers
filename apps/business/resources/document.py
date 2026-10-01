from import_export import resources

from apps.business.models import BusinessDocument


class BusinessDocumentResource(
    resources.ModelResource
):

    class Meta:

        model = BusinessDocument

        import_id_fields = (
            "id",
        )