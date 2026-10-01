from django.apps import AppConfig


class BusinessUtilityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.business_utility"
    verbose_name = "Business Utility"

    def ready(self):
        import apps.business_utility.admin