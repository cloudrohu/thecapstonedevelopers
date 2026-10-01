from import_export import resources

from apps.business.models import (
    BusinessEnquiry,
)


class BusinessEnquiryResource(
    resources.ModelResource
):

    class Meta:

        model = BusinessEnquiry

        import_id_fields = (
            "id",
        )