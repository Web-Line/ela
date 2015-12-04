from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger("ela")


def create_notice_types(sender, **kwargs):
    """
    define NoticeType for this app
    """
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        logger.debug("Creating notices for ela")
        NoticeType.create("signup_user", _("User Signup"),
                          _("an user join to ela"))
    #     ... for more notice type
    else:
        logger.debug("Skipping creation of NoticeTypes as notification app not "
                     "found")


def handle_post_migrate(sender, **kwargs):
    """
    It sets up a superuser when DEBUG is True.
    :param sender:
    :param kwargs:
    :return:
    """
    logger.debug('Handling post_migrate signal, DEBUG={}, interactive={}'.format(
        settings.DEBUG, kwargs['interactive']))
    if settings.DEBUG and kwargs['interactive']:
        get_user_model().objects.create_superuser(123, "arc", "Karami",
                                                            "arc@arc.ir", 123)
    #
    create_notice_types(sender)


class WUserAppConfig(AppConfig):
    name = 'wuser'
    verbose_name = _("Authentication")

    def ready(self):
        post_migrate.connect(handle_post_migrate, sender=self)
        from wuser.signals import handle_user_logged_in