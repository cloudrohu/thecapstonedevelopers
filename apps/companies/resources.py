from import_export import resources

from .models import (
    Company,
    Branch,
    Department,
    Designation,
    CompanyContact,
    CompanyDocument,
    CompanyGallery,   # <-- Add this
)


class CompanyResource(resources.ModelResource):

    class Meta:
        model = Company
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("id",)
        exclude = (
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )


class BranchResource(resources.ModelResource):

    class Meta:
        model = Branch
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("id",)


class DepartmentResource(resources.ModelResource):

    class Meta:
        model = Department
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("id",)


class DesignationResource(resources.ModelResource):

    class Meta:
        model = Designation
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("id",)


class CompanyContactResource(resources.ModelResource):

    class Meta:
        model = CompanyContact
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("id",)


class CompanyDocumentResource(resources.ModelResource):

    class Meta:
        model = CompanyDocument
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("id",)


class CompanyGalleryResource(resources.ModelResource):

    class Meta:
        model = CompanyGallery
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("id",)