from import_export import resources

from apps.business.models import (
    BusinessAttributeValue,
)


class BusinessAttributeValueResource(
    resources.ModelResource
):

    class Meta:

        model = BusinessAttributeValue

        import_id_fields = (
            "id",
        )