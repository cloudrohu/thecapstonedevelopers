from import_export import resources

from apps.business.models import (
    BusinessMeeting,
)


class BusinessMeetingResource(
    resources.ModelResource
):

    class Meta:

        model = BusinessMeeting

        import_id_fields = (
            "id",
        )