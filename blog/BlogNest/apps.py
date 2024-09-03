from django.apps import AppConfig


class BlogNestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BlogNest'

    def ready(self):
        import BlogNest.signals
