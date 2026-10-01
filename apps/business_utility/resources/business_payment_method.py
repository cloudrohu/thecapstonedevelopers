from import_export import resources

from apps.business_utility.models import BusinessPaymentMethod


class BusinessPaymentMethodResource(resources.ModelResource):

    class Meta:

        model = BusinessPaymentMethod

        import_id_fields = (
            "id",
        )

        skip_unchanged = True

        report_skipped = True