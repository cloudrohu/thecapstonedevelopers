from import_export import resources

from apps.business.models import (
    BusinessSocialLink,
)


class BusinessSocialLinkResource(
    resources.ModelResource
):

    class Meta:

        model = BusinessSocialLink

        import_id_fields = (
            "id",
        )