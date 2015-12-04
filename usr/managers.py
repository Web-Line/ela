from django.db import models
from usr.roles import (Student, Teacher, Supervisor)
from django.contrib.auth.models import BaseUserManager
import logging

logger = logging.getLogger("ela")


class UserManager(BaseUserManager):
    def create_user(self, national_id, first_name, last_name, email,
                    password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        logger.debug(
            "national_id='{}', first_name='{}', last_name='{}', email='{}',"
            " password='{}'".format(national_id, first_name, last_name, email,
                                    password))
        if not national_id:
            raise ValueError('Users must provide a national id')

        user = self.model(national_id=str(national_id), first_name=first_name,
                          last_name=last_name, email=email)

        user.set_password(password)
        user.is_admin = False
        user.save(using=self._db)
        return user

    def create_superuser(self, national_id, first_name, last_name, email,
                         password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        logger.debug(
            "national_id='{}', first_name='{}', last_name='{}', email='{}',"
            " password='{}'".format(national_id, first_name, last_name, email,
                                    password))

        user = self.create_user(national_id, first_name=first_name,
                                last_name=last_name, email=email,
                                password=password)
        user.is_admin, user.is_staff, user.is_superuser = True, True, True
        user.save(using=self._db)
        # user.confirm_email(user.confirmation_key)
        return user


class StudentManager(models.Manager):
    def get_queryset(self):
        """
        Filter user with have student role.
        """
        return super(StudentManager, self).get_queryset().filter(
            groups__name=Student.get_name())


class TeacherManager(models.Manager):
    def get_queryset(self):
        """
        Filter user with have teacher role.
        """
        return super(TeacherManager, self).get_queryset().filter(
            groups__name=Teacher.get_name())


class SupervisorManager(models.Manager):
    def get_queryset(self):
        """
        Filter user with have supervisor manager role.
        """
        return super(SupervisorManager, self).get_queryset().filter(
            groups__name=Supervisor.get_name())
