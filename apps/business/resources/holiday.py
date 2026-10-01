from import_export import resources

from apps.business.models import BusinessHoliday


class BusinessHolidayResource(
    resources.ModelResource
):

    class Meta:

        model = BusinessHoliday

        import_id_fields = (
            "id",
        )