from import_export import resources

from apps.business.models import BusinessTiming


class BusinessTimingResource(
    resources.ModelResource
):

    class Meta:

        model = BusinessTiming

        import_id_fields = (
            "id",
        )