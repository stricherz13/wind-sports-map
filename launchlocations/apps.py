from django.apps import AppConfig


class LaunchlocationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "launchlocations"

    def ready(self):
        import launchlocations.signals  # Ensure the signals are imported
