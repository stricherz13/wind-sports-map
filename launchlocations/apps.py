from django.apps import AppConfig


class LaunchLocationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'launchlocations'

    def ready(self):
        import launchlocations.signals  # noqa
