from import_export import resources

from apps.business.models import (
    BusinessFollowUp,
)


class BusinessFollowUpResource(
    resources.ModelResource
):

    class Meta:

        model = BusinessFollowUp

        import_id_fields = (
            "id",
        )