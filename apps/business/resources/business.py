from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from apps.business.models import Business
from apps.utility.models import Location

from apps.business_utility.models import (
    BusinessCategory,
    BusinessType,
    BusinessChain,
)


class BusinessResource(resources.ModelResource):

    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(
            BusinessCategory,
            "name",
        ),
    )

    business_type = fields.Field(
        column_name="business_type",
        attribute="business_type",
        widget=ForeignKeyWidget(
            BusinessType,
            "name",
        ),
    )

    chain = fields.Field(
        column_name="chain",
        attribute="chain",
        widget=ForeignKeyWidget(
            BusinessChain,
            "name",
        ),
    )

    location = fields.Field(
        column_name="location",
        attribute="location",
        widget=ForeignKeyWidget(
            Location,
            "name",
        ),
    )

    class Meta:

        model = Business

        import_id_fields = (
            "id",
        )

        skip_unchanged = True

        report_skipped = True