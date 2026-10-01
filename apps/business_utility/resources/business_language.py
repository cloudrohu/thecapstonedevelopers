from import_export import resources

from apps.business_utility.models import BusinessLanguage


class BusinessLanguageResource(resources.ModelResource):

    class Meta:

        model = BusinessLanguage

        import_id_fields = (
            "id",
        )

        skip_unchanged = True

        report_skipped = True