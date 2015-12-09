from rolepermissions.roles import AbstractUserRole
from django.conf import settings


class StudentRole(AbstractUserRole):
    available_permissions = [
        settings.LOGIN_STUDENT_ADMIN_SITE,
    ]


class TeacherRole(AbstractUserRole):
    available_permissions = [
        settings.LOGIN_TEACHER_ADMIN_SITE,
    ]


class SupervisorRole(AbstractUserRole):
    available_permissions = [
        settings.LOGIN_SUPERVISOR_ADMIN_SITE,
    ]
