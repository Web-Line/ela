from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger("ela")

def setup_superuser(sender, **kwargs):
    logger.debug('Handling post_migrate signal, DEBUG={}, interactive={}'.format(
        settings.DEBUG, kwargs['interactive']))
    if settings.DEBUG and kwargs['interactive']:
        get_user_model().objects.create_superuser(123, "arc", "Karami",
                                                            "arc@arc.ir", 123)


class WUserAppConfig(AppConfig):
    name = 'wuser'
    verbose_name = _("Authentication and Authorization")

    def ready(self):
        post_migrate.connect(setup_superuser, sender=self)