import logging
from django.db import models
from ela.roles import (StudentRole, TeacherRole, SupervisorRole)

logger = logging.getLogger("ela")


class StudentManager(models.Manager):
    def get_queryset(self):
        """
        Filter user with have student role.
        """
        return super(StudentManager, self).get_queryset().filter(
            groups__name=StudentRole.get_name())


class TeacherManager(models.Manager):
    def get_queryset(self):
        """
        Filter user with have teacher role.
        """
        return super(TeacherManager, self).get_queryset().filter(
            groups__name=TeacherRole.get_name())


class SupervisorManager(models.Manager):
    def get_queryset(self):
        """
        Filter user with have supervisor manager role.
        """
        return super(SupervisorManager, self).get_queryset().filter(
            groups__name=SupervisorRole.get_name())
