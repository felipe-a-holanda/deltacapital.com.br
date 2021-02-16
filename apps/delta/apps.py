from django.apps import AppConfig


class DeltaConfig(AppConfig):
    name = "apps.delta"

    def ready(self):
        try:
            import apps.delta.signals  # noqa F401
        except ImportError:
            pass

