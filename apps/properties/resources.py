from import_export import resources, fields

from .models import (
    Developer,
    Meeting,
    Followup
)


class DeveloperResource(resources.ModelResource):

    class Meta:
        model = Developer
        fields = (
            "id",
            "title",
            "city",
            "locality",
            "area",
            "postal_code",
            "address",
            "contact_person",
            "contact_no",
            "email",
            "google_map",
            "web_site",
            "keywords",
            "about_developer",
            "note",
            "featured_builder",
            "is_verified",
            "is_featured",
            "calling_status",
            "assigned_to",
            "slug",
            "is_active",
            "created_at",
            "updated_at",
        )


class MeetingResource(resources.ModelResource):

    meeting_id = fields.Field(
        attribute="id",
        column_name="Meeting ID",
    )

    meeting_type = fields.Field(
        attribute="type",
        column_name="Meeting Type",
    )

    meeting_status = fields.Field(
        attribute="status",
        column_name="Meeting Status",
    )

    meeting_date_export = fields.Field(
        attribute="meeting_date",
        column_name="Meeting Date",
    )

    assigned_to_export = fields.Field(
        attribute="assigned_to",
        column_name="Assigned To",
    )

    comment_export = fields.Field(
        attribute="comment",
        column_name="Comment",
    )

    # =====================================================
    # PARENT
    # =====================================================

    parent_type = fields.Field(
        column_name="Parent Type",
    )

    parent_id = fields.Field(
        column_name="Parent ID",
    )

    parent_name = fields.Field(
        column_name="Parent Name",
    )

    parent_contact_person = fields.Field(
        column_name="Parent Contact Person",
    )

    parent_contact_no = fields.Field(
        column_name="Parent Contact No",
    )

    parent_email = fields.Field(
        column_name="Parent Email",
    )

    parent_city = fields.Field(
        column_name="Parent City",
    )

    parent_locality = fields.Field(
        column_name="Parent Locality",
    )

    parent_area = fields.Field(
        column_name="Parent Area",
    )

    parent_postal_code = fields.Field(
        column_name="Parent Postal Code",
    )

    parent_address = fields.Field(
        column_name="Parent Address",
    )

    parent_website = fields.Field(
        column_name="Parent Website",
    )

    # =====================================================
    # DEVELOPER
    # =====================================================

    developer_name = fields.Field(
        column_name="Developer Name",
    )

    developer_contact_person = fields.Field(
        column_name="Developer Contact Person",
    )

    developer_contact_no = fields.Field(
        column_name="Developer Contact No",
    )

    developer_email = fields.Field(
        column_name="Developer Email",
    )

    # =====================================================
    # ARCHITECT
    # =====================================================

    architect_name = fields.Field(
        column_name="Architect Name",
    )

    architect_contact_person = fields.Field(
        column_name="Architect Contact Person",
    )

    architect_contact_no = fields.Field(
        column_name="Architect Contact No",
    )

    architect_email = fields.Field(
        column_name="Architect Email",
    )

    # =====================================================
    # ENGINEER
    # =====================================================

    engineer_name = fields.Field(
        column_name="Engineer Name",
    )

    engineer_contact_person = fields.Field(
        column_name="Engineer Contact Person",
    )

    engineer_contact_no = fields.Field(
        column_name="Engineer Contact No",
    )

    engineer_email = fields.Field(
        column_name="Engineer Email",
    )

    # =====================================================
    # HELPER
    # =====================================================

    def get_parent(self, obj):

        if obj.developer:
            return obj.developer

        if obj.architect:
            return obj.architect

        if obj.engineer:
            return obj.engineer

        if obj.project:
            return obj.project

        return None

    # =====================================================
    # PARENT
    # =====================================================

    def dehydrate_parent_type(self, obj):

        if obj.developer:
            return "Developer"

        if obj.architect:
            return "Architect"

        if obj.engineer:
            return "Engineer"

        if obj.project:
            return "Project"

        return "-"

    def dehydrate_parent_id(self, obj):

        parent = self.get_parent(obj)

        return parent.pk if parent else "-"

    def dehydrate_parent_name(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        if hasattr(parent, "title"):
            return parent.title

        if hasattr(parent, "project_name"):
            return parent.project_name

        return str(parent)

    def dehydrate_parent_contact_person(self, obj):

        parent = self.get_parent(obj)

        return getattr(parent, "contact_person", None) or "-" if parent else "-"

    def dehydrate_parent_contact_no(self, obj):

        parent = self.get_parent(obj)

        return getattr(parent, "contact_no", None) or "-" if parent else "-"

    def dehydrate_parent_email(self, obj):

        parent = self.get_parent(obj)

        return getattr(parent, "email", None) or "-" if parent else "-"

    def dehydrate_parent_city(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        value = getattr(parent, "city", None)

        return str(value) if value else "-"

    def dehydrate_parent_locality(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        value = getattr(parent, "locality", None)

        return str(value) if value else "-"

    def dehydrate_parent_area(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        value = getattr(parent, "area", None)

        return str(value) if value else "-"

    def dehydrate_parent_postal_code(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        value = getattr(parent, "postal_code", None)

        return str(value) if value else "-"

    def dehydrate_parent_address(self, obj):

        parent = self.get_parent(obj)

        return getattr(parent, "address", None) or "-" if parent else "-"

    def dehydrate_parent_website(self, obj):

        parent = self.get_parent(obj)

        return getattr(parent, "web_site", None) or "-" if parent else "-"

    # =====================================================
    # DEVELOPER
    # =====================================================

    def dehydrate_developer_name(self, obj):

        return obj.developer.title if obj.developer else "-"

    def dehydrate_developer_contact_person(self, obj):

        return obj.developer.contact_person or "-" if obj.developer else "-"

    def dehydrate_developer_contact_no(self, obj):

        return obj.developer.contact_no or "-" if obj.developer else "-"

    def dehydrate_developer_email(self, obj):

        return obj.developer.email or "-" if obj.developer else "-"

    # =====================================================
    # ARCHITECT
    # =====================================================

    def dehydrate_architect_name(self, obj):

        return obj.architect.title if obj.architect else "-"

    def dehydrate_architect_contact_person(self, obj):

        return obj.architect.contact_person or "-" if obj.architect else "-"

    def dehydrate_architect_contact_no(self, obj):

        return obj.architect.contact_no or "-" if obj.architect else "-"

    def dehydrate_architect_email(self, obj):

        return obj.architect.email or "-" if obj.architect else "-"

    # =====================================================
    # ENGINEER
    # =====================================================

    def dehydrate_engineer_name(self, obj):

        return obj.engineer.title if obj.engineer else "-"

    def dehydrate_engineer_contact_person(self, obj):

        return obj.engineer.contact_person or "-" if obj.engineer else "-"

    def dehydrate_engineer_contact_no(self, obj):

        return obj.engineer.contact_no or "-" if obj.engineer else "-"

    def dehydrate_engineer_email(self, obj):

        return obj.engineer.email or "-" if obj.engineer else "-"

    # =====================================================
    # META
    # =====================================================

    class Meta:

        model = Meeting

        fields = (
            "meeting_id",
            "meeting_type",
            "meeting_status",
            "meeting_date_export",
            "assigned_to_export",
            "comment_export",

            "parent_type",
            "parent_id",
            "parent_name",
            "parent_contact_person",
            "parent_contact_no",
            "parent_email",
            "parent_city",
            "parent_locality",
            "parent_area",
            "parent_postal_code",
            "parent_address",
            "parent_website",

            "developer_name",
            "developer_contact_person",
            "developer_contact_no",
            "developer_email",

            "architect_name",
            "architect_contact_person",
            "architect_contact_no",
            "architect_email",

            "engineer_name",
            "engineer_contact_person",
            "engineer_contact_no",
            "engineer_email",
        )


# =====================================================
# FOLLOWUP RESOURCE
# =====================================================

class FollowupResource(resources.ModelResource):

    followup_id = fields.Field(
        attribute="id",
        column_name="Followup ID",
    )

    followup_type = fields.Field(
        attribute="type",
        column_name="Followup Type",
    )

    followup_status = fields.Field(
        attribute="status",
        column_name="Followup Status",
    )

    followup_date_export = fields.Field(
        attribute="followup_date",
        column_name="Followup Date",
    )

    assigned_to_export = fields.Field(
        attribute="assigned_to",
        column_name="Assigned To",
    )

    comment_export = fields.Field(
        attribute="comment",
        column_name="Comment",
    )

    # =====================================================
    # PARENT
    # =====================================================

    parent_type = fields.Field(
        column_name="Parent Type",
    )

    parent_id = fields.Field(
        column_name="Parent ID",
    )

    parent_name = fields.Field(
        column_name="Parent Name",
    )

    parent_contact_person = fields.Field(
        column_name="Parent Contact Person",
    )

    parent_contact_no = fields.Field(
        column_name="Parent Contact No",
    )

    parent_email = fields.Field(
        column_name="Parent Email",
    )

    parent_city = fields.Field(
        column_name="Parent City",
    )

    parent_locality = fields.Field(
        column_name="Parent Locality",
    )

    parent_area = fields.Field(
        column_name="Parent Area",
    )

    parent_postal_code = fields.Field(
        column_name="Parent Postal Code",
    )

    parent_address = fields.Field(
        column_name="Parent Address",
    )

    parent_website = fields.Field(
        column_name="Parent Website",
    )

    # =====================================================
    # DEVELOPER
    # =====================================================

    developer_name = fields.Field(
        column_name="Developer Name",
    )

    developer_contact_person = fields.Field(
        column_name="Developer Contact Person",
    )

    developer_contact_no = fields.Field(
        column_name="Developer Contact No",
    )

    developer_email = fields.Field(
        column_name="Developer Email",
    )

    # =====================================================
    # ARCHITECT
    # =====================================================

    architect_name = fields.Field(
        column_name="Architect Name",
    )

    architect_contact_person = fields.Field(
        column_name="Architect Contact Person",
    )

    architect_contact_no = fields.Field(
        column_name="Architect Contact No",
    )

    architect_email = fields.Field(
        column_name="Architect Email",
    )

    # =====================================================
    # ENGINEER
    # =====================================================

    engineer_name = fields.Field(
        column_name="Engineer Name",
    )

    engineer_contact_person = fields.Field(
        column_name="Engineer Contact Person",
    )

    engineer_contact_no = fields.Field(
        column_name="Engineer Contact No",
    )

    engineer_email = fields.Field(
        column_name="Engineer Email",
    )

    # =====================================================
    # HELPER
    # =====================================================

    def get_parent(self, obj):

        if obj.developer:
            return obj.developer

        if obj.architect:
            return obj.architect

        if obj.engineer:
            return obj.engineer

        if obj.project:
            return obj.project

        return None

    # =====================================================
    # PARENT DETAILS
    # =====================================================

    def dehydrate_parent_type(self, obj):

        if obj.developer:
            return "Developer"

        if obj.architect:
            return "Architect"

        if obj.engineer:
            return "Engineer"

        if obj.project:
            return "Project"

        return "-"

    def dehydrate_parent_id(self, obj):

        parent = self.get_parent(obj)

        return parent.pk if parent else "-"

    def dehydrate_parent_name(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        if hasattr(parent, "title"):
            return parent.title

        if hasattr(parent, "project_name"):
            return parent.project_name

        return str(parent)

    def dehydrate_parent_contact_person(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        return getattr(parent, "contact_person", None) or "-"

    def dehydrate_parent_contact_no(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        return getattr(parent, "contact_no", None) or "-"

    def dehydrate_parent_email(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        return getattr(parent, "email", None) or "-"

    def dehydrate_parent_city(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        value = getattr(parent, "city", None)

        return str(value) if value else "-"

    def dehydrate_parent_locality(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        value = getattr(parent, "locality", None)

        return str(value) if value else "-"

    def dehydrate_parent_area(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        value = getattr(parent, "area", None)

        return str(value) if value else "-"

    def dehydrate_parent_postal_code(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        value = getattr(parent, "postal_code", None)

        return str(value) if value else "-"

    def dehydrate_parent_address(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        return getattr(parent, "address", None) or "-"

    def dehydrate_parent_website(self, obj):

        parent = self.get_parent(obj)

        if not parent:
            return "-"

        return getattr(parent, "web_site", None) or "-"

    # =====================================================
    # DEVELOPER
    # =====================================================

    def dehydrate_developer_name(self, obj):
        return obj.developer.title if obj.developer else "-"

    def dehydrate_developer_contact_person(self, obj):
        return obj.developer.contact_person or "-" if obj.developer else "-"

    def dehydrate_developer_contact_no(self, obj):
        return obj.developer.contact_no or "-" if obj.developer else "-"

    def dehydrate_developer_email(self, obj):
        return obj.developer.email or "-" if obj.developer else "-"

    # =====================================================
    # ARCHITECT
    # =====================================================

    def dehydrate_architect_name(self, obj):
        return obj.architect.title if obj.architect else "-"

    def dehydrate_architect_contact_person(self, obj):
        return obj.architect.contact_person or "-" if obj.architect else "-"

    def dehydrate_architect_contact_no(self, obj):
        return obj.architect.contact_no or "-" if obj.architect else "-"

    def dehydrate_architect_email(self, obj):
        return obj.architect.email or "-" if obj.architect else "-"

    # =====================================================
    # ENGINEER
    # =====================================================

    def dehydrate_engineer_name(self, obj):
        return obj.engineer.title if obj.engineer else "-"

    def dehydrate_engineer_contact_person(self, obj):
        return obj.engineer.contact_person or "-" if obj.engineer else "-"

    def dehydrate_engineer_contact_no(self, obj):
        return obj.engineer.contact_no or "-" if obj.engineer else "-"

    def dehydrate_engineer_email(self, obj):
        return obj.engineer.email or "-" if obj.engineer else "-"

    # =====================================================
    # META
    # =====================================================

    class Meta:

        model = Followup

        fields = (
            "followup_id",
            "followup_type",
            "followup_status",
            "followup_date_export",
            "assigned_to_export",
            "comment_export",

            "parent_type",
            "parent_id",
            "parent_name",
            "parent_contact_person",
            "parent_contact_no",
            "parent_email",
            "parent_city",
            "parent_locality",
            "parent_area",
            "parent_postal_code",
            "parent_address",
            "parent_website",

            "developer_name",
            "developer_contact_person",
            "developer_contact_no",
            "developer_email",

            "architect_name",
            "architect_contact_person",
            "architect_contact_no",
            "architect_email",

            "engineer_name",
            "engineer_contact_person",
            "engineer_contact_no",
            "engineer_email",
        )
