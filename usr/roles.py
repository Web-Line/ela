from __future__ import unicode_literals
from django.conf import settings
from rolepermissions.roles import AbstractUserRole, RolesClassRegister
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from usr.models import User
from six import add_metaclass
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rolepermissions.utils import camelToSnake


class Student(AbstractUserRole):
    """
    """
    available_permissions = {
        'visit_profile': True,
    }

    # objects = StudentManager()

    # def profile_complete(self):
    #     """
    #     Check profile of student and Student information if both of them is
    #     fill True return True else False.
    #     """
    #     return self.profile is not None and self.profile.is_fill and self.student_info is not None and self.student_info.is_fill
    # profile_complete.boolean = True
    # profile_complete.admin_order_field = ['profile__is_fill', 'student_info__is_fill']
    #
    # def active_student(self):
    #     """
    #     if Student is in Student group(who are registered completely) return
    #     True or False.
    #     """
    #     return self.groups.filter(name="Student").exists()
    # active_student.boolean = True
    # active_student.admin_order_field = 'groups'

    # def register_student(self):
    #     stu_group = Group.objects.get(name='Student')
    #     self.groups = [stu_group]
    #     self.save()
    #
    # def unregistered_student(self):
    #     stu_group = Group.objects.get(name='BaseStudent')
    #     self.groups = [stu_group]
    #     self.save()
    #
    # def get_absolute_url_admin(self):
    #     return reverse('admin-panel:accounts_student_change', args=(self.id,))
    #
    # class Meta:
    #     proxy = True
    #     permissions = (("student", "have student permission"),)
    #     verbose_name = _("Student")
    #     verbose_name_plural = _("Students")
