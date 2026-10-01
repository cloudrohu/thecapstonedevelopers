from django.apps import AppConfig


class ResponseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.response'

    def ready(self):
        import apps.response.signals



    



    
