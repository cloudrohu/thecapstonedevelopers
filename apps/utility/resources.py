from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Location


class LocationResource(resources.ModelResource):

    parent = fields.Field(
        column_name="parent",
        attribute="parent",
        widget=ForeignKeyWidget(Location, "id"),   # ✅ id, name nahi
    )

    class Meta:
        model = Location

        import_id_fields = ("id",)

        exclude = (
            "lft",
            "rght",
            "tree_id",
            "level",
        )

        skip_unchanged = True
        report_skipped = True