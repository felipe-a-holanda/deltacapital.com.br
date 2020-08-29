from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "apps.users"
    verbose_name = _("Usuários")
    verbose_name_plural = _("Usuários")

    def ready(self):
        try:
            import apps.users.signals  # noqa F401
        except ImportError:
            pass
