from import_export import resources

from apps.business.models import BusinessGallery


class BusinessGalleryResource(
    resources.ModelResource
):

    class Meta:

        model = BusinessGallery

        import_id_fields = (
            "id",
        )