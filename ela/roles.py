from rolepermissions.roles import AbstractUserRole
from django.conf import settings


class StudentRole(AbstractUserRole):
    role_name = settings.STUDENT_ROLE_GROUP_NAME
    available_permissions = {
        settings.LOGIN_STUDENT_ADMIN_SITE: True
    }


class TeacherRole(AbstractUserRole):
    role_name = settings.TEACHER_ROLE_GROUP_NAME
    available_permissions = {
        settings.LOGIN_TEACHER_ADMIN_SITE: True,
    }


class SupervisorRole(AbstractUserRole):
    role_name = settings.SUPERVISOR_ROLE_GROUP_NAME
    available_permissions = {
        settings.LOGIN_SUPERVISOR_ADMIN_SITE: True,
    }
