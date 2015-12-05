from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
from appconf import AppConf
import logging

logger = logging.getLogger("ela")


class EduAppConfig(AppConfig):
    name = "edu"
    verbose_name = _("Authentication")

    def ready(self):
        pass


class EduAppConf(AppConf):
    EDU_LANGUAGES = [("en", _("English")), ("fa", _("Farsi"))]
    EDU_DEFAULT_LANGUAGE = "en"

    COURSE_STATUS_HOLDING_ON_WAIT = 11
    COURSE_STATUS_HOLDING_ACTIVELY = 22
    COURSE_STATUS_HOLDING_ACCOMPLISHED = 33
    COURSE_STATUS = {
        COURSE_STATUS_HOLDING_ON_WAIT: _("Waiting"),
        COURSE_STATUS_HOLDING_ACTIVELY: _("Holding"),
        COURSE_STATUS_HOLDING_ACCOMPLISHED: _("Finished"),
    }

    TRANSCRIPT_STATUS_PASS = 44
    TRANSCRIPT_STATUS_FAIL = 55
    TRANSCRIPT_STATUS_CONDITIONAL = 55

    TRANSCRIPT_STATUS = {
        TRANSCRIPT_STATUS_PASS: _("Pass"),
        TRANSCRIPT_STATUS_FAIL: _("Fail"),
        TRANSCRIPT_STATUS_CONDITIONAL: _("Conditional"),
    }

    TRANSCRIPT_PASS_VALUE = 70
    TRANSCRIPT_FAIL_VALUE = 50
    TRANSCRIPT_CONDITIONAL_VALUE = (
        TRANSCRIPT_FAIL_VALUE,
        TRANSCRIPT_PASS_VALUE
    )



