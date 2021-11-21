from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersAppConfig(AppConfig):
    """Configuration for Users app."""

    name = 'apps.users'
    verbose_name = _('Users')

    def ready(self):
        from .api.auth import scheme  # noqa
