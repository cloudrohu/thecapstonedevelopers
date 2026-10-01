from import_export import resources

from apps.business.models import (
    BusinessReview,
)


class BusinessReviewResource(
    resources.ModelResource
):

    class Meta:

        model = BusinessReview

        import_id_fields = (
            "id",
        )