from django.utils.translation import ugettext_lazy as _
from ela.managers import (StudentManager, TeacherManager, SupervisorManager)
from usr.models import User


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = _("Student")
        verbose_name_plural = _("Students")


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")


class Supervisor(User):
    objects = SupervisorManager()

    class Meta:
        proxy = True
        verbose_name = _("Supervisor")
        verbose_name_plural = _("Supervisors")
