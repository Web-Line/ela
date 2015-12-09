from importlib import import_module
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings
import logging

logger = logging.getLogger("ela")

logger.debug("loading ela/apps.py")

def handle_post_migrate(sender, **kwargs):
    """
    Set up groups after migration and group permissions when DEBUG is
    True.
    :param sender:
    :param kwargs:
    :return:
    """
    logger.debug("ela_handler_post_migrations is called")
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import (Permission, Group)
    from usr.models import User
    from ela.roles import (StudentRole, TeacherRole, SupervisorRole)
    from rolepermissions.verifications import has_permission
    from ela.forms import (
        MainAdminAuthenticationForm,
        StudentAdminAuthenticationForm,
        TeacherAdminAuthenticationForm,
        SupervisorAdminAuthenticationForm
    )

    logger.debug(
        'Handling post_migrate signal. '
        'DEBUG={}, interactive={}'.format(
            settings.DEBUG,
            kwargs['interactive'])
    )

    # Getting groups
    student_group = Group.objects.create(
        name=settings.STUDENT_ROLE_GROUP_NAME
    )
    teacher_group = Group.objects.create(
        name=settings.TEACHER_ROLE_GROUP_NAME
    )
    supervisor_group = Group.objects.create(
        name=settings.SUPERVISOR_ROLE_GROUP_NAME
    )

    logger.debug(
        "student_group={}, "
        "teacher_group={}, "
        "supervisor_group={}".format(
            student_group,
            teacher_group,
            supervisor_group
        )
    )

    if settings.DEBUG:
        # Setting up initial users
        superuser = User.objects.create_superuser(
            "admin",
            "Arsalan",
            "Karami",
            "arc@ela.ir",
            "test",
        )

        staff = User.objects.create_user(
            "staff",
            "Ms",
            "Kashani",
            "kashani@ela.ir",
            "test",
        )

        student1 = User.objects.create_user(
            "student1",
            "Mohammad",
            "Haghighat",
            "mhg@ela.ir",
            "test",
        )

        student2 = User.objects.create_user(
            "student2",
            "Alireza",
            "Molaee",
            "mol@ela.ir",
            "test",
        )

        teacher = User.objects.create_user(
            "teacher",
            "Sina",
            "Amini",
            "sina@ela.ir",
            "test",
        )

        supervisor = User.objects.create_user(
            "supervisor",
            "Masoud",
            "Pirbodaqi",
            "masoud@ela.ir",
            "test"
        )

        # Modifying user is_active flag.
        superuser.is_active = True
        staff.is_active = True
        student1.is_active = True
        student2.is_active = False
        teacher.is_active = True
        supervisor.is_active = True

        staff.is_staff = True

        # Saving users
        superuser.save()
        staff.save()
        student1.save()
        student2.save()
        teacher.save()
        supervisor.save()

        # Assigning role (group) to each user.
        StudentRole.assign_role_to_user(student1)
        StudentRole.assign_role_to_user(student2)

        TeacherRole.assign_role_to_user(teacher)
        SupervisorRole.assign_role_to_user(supervisor)

        logger.debug("superuser={}".format(superuser))
        logger.debug("staff={}".format(staff))
        logger.debug("student1={}".format(student1))
        logger.debug("student2={}".format(student2))
        logger.debug("teacher={}".format(teacher))
        logger.debug("supervisor={}".format(supervisor))

        # Check if users can login into their account
        main_admin_authentication_form = MainAdminAuthenticationForm()
        student_admin_authentication_form = StudentAdminAuthenticationForm()
        teacher_admin_authentication_form = TeacherAdminAuthenticationForm()
        supervisor_admin_authentication_form = \
            SupervisorAdminAuthenticationForm()

        logger.debug("Checking superuser")
        main_admin_authentication_form.confirm_login_allowed(superuser)

        logger.debug("Checking staff")
        main_admin_authentication_form.confirm_login_allowed(staff)

        logger.debug("Checking student1")
        student_admin_authentication_form.confirm_login_allowed(student1)

        logger.debug("Checking student2")
        student_admin_authentication_form.confirm_login_allowed(student2)

        logger.debug("Checking teacher")
        teacher_admin_authentication_form.confirm_login_allowed(teacher)

        logger.debug("Checking supervisor")
        supervisor_admin_authentication_form.confirm_login_allowed(supervisor)

        # auth_content_type = ContentType.objects.get(
        #     app_label="usr",
        #     model="user"
        # )
        #
        # logger.debug("auth_content_type={}".format(auth_content_type.id))
        #
        # # Creating necessary permissions
        # student_login_perm = Permission.objects.get(
        #     codename=settings.LOGIN_STUDENT_ADMIN_SITE,
        #     content_type=auth_content_type
        # )
        # teacher_login_perm = Permission.objects.get(
        #     codename=settings.LOGIN_TEACHER_ADMIN_SITE,
        #     content_type=auth_content_type
        # )
        # supervisor_login_perm = Permission.objects.get(
        #     codename=settings.LOGIN_SUPERVISOR_ADMIN_SITE,
        #     content_type=auth_content_type,
        # )
        #
        # logger.debug(
        #     "student_login_perm={}, "
        #     "teacher_login_perm={}, "
        #     "supervisor_login_perm={}".format(
        #         student_login_perm,
        #         teacher_login_perm,
        #         supervisor_login_perm
        #     ))
        #
        # # Assigning permissions to groups
        # student_group.permissions.add(student_login_perm)
        # teacher_group.permissions.add(teacher_login_perm)
        # supervisor_group.permissions.add(supervisor_login_perm)
        #
        # logger.debug(
        #     "student_group permissions={}, "
        #     "teacher_group permissions={}, "
        #     "supervisor_group permissions={}, ".format(
        #         student_group.permissions.all(),
        #         teacher_group.permissions.all(),
        #         supervisor_group.permissions.all()
        #     )
        # )


class ElaAppConfig(AppConfig):
    name = "ela"

    def ready(self):
        logger.debug("ela is ready")

        post_migrate.connect(handle_post_migrate)
        import_module("ela.receivers")
