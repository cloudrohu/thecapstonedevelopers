from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from apps.business_utility.models import BusinessCategory


class BusinessCategoryResource(resources.ModelResource):

    parent = fields.Field(
        column_name="parent",
        attribute="parent",
        widget=ForeignKeyWidget(
            BusinessCategory,
            "id",
        ),
    )

    class Meta:
        model = BusinessCategory

        import_id_fields = (
            "id",
        )

        exclude = (
            "lft",
            "rght",
            "tree_id",
            "level",
        )

        skip_unchanged = True
        report_skipped = True