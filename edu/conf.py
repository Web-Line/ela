from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
from appconf import AppConf
import logging

logger = logging.getLogger("ela")


class EduAppConfig(AppConfig):
    name = 'edu'
    verbose_name = _("Authentication")

    def ready(self):
        pass


class EduAppConf(AppConf):
    EDU_LANGUAGES = [('en', 'English'), ('fa', 'Farsi')]