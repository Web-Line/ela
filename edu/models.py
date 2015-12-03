# from datetime import datetime
# from django.utils.timezone import now
from datetime import datetime

from django.core.validators import MinValueValidator as Min
from django.db import models
# from django.core.validators import ValidationError
from django.conf import settings
# from django.template.defaultfilters import filesizeformat
# from django.utils.html import format_html
# from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from wuser.roles import Student
# from django.core.validators import MaxValueValidator


class Edu(models.Model):
    name = models.CharField(_("name"), max_length=30)
    language = models.CharField(_("language"), max_length=30,
                                choices=settings.EDU_LANGUAGES,
                                default=settings.LANGUAGE_CODE)

    class Meta():
        verbose_name = "Education System"
        verbose_name_plural = "Education Systems"

    def __unicode__(self):
        return "%s %s" % (self.name, self.language)

    # def no_of_levels(self):
    #     return Level.objects.filter(edu=self).count()
    #
    # def no_of_terms(self):
    #     return Term.objects.filter(level__edu=self).count()
    #
    # def no_of_sessions(self):
    #     return Session.objects.filter(term__level__edu=self).count()
    #
    # def level_of_student(self, stu):
    #     resumes = stu.studentresume_set.filter(term__level__edu=self).order_by('-date')
    #     last_level = resumes[0].term.level
    #     per_last_level = resumes[1].term.level
    #     base_level = stu.baselevel_set.get(edu=self).level
    #     i = last_level.index + 1
    #     try:
    #         next_level = self.level_set.get(index=i)
    #     except:
    #         next_level = None
    #     if not last_level and not base_level:
    #         return self.level_set.get(index=1)
    #     if base_level and not last_level:
    #         return base_level
    #     if base_level and last_level and base_level.index > last_level.index:
    #         return base_level
    #     if resumes[0].resume_status == StudentResume.PASSED:
    #         return next_level
    #     if resumes[1].resume_status == StudentResume.PASSED_CONDITIONALLY:
    #         return per_last_level
    #     if resumes[0].resume_status == StudentResume.PASSED_CONDITIONALLY:
    #         return next_level
    #     if resumes[0].resume_status == StudentResume.FAILED:
    #         return last_level



class Level(models.Model):
    edu = models.ForeignKey(Edu,verbose_name=_("education system"))
    name = models.CharField(_("name"), max_length=30)
    index = models.IntegerField(_("index"), validators=[Min(0)])
    tuition = models.FloatField(_("tuition"), null=True, blank=True)
    capacity = models.IntegerField(_("capacity"), null=True, blank=True)
    description = models.TextField(_("description"), max_length=250, null=True,
                                   blank=True)

    # def no_of_terms(self):
    #     return Term.objects.filter(level=self).count()

    def __unicode__(self):
        return self.name


# class Material(models.Model):
#     name = models.CharField(max_length=254, unique=True)
#     file = models.FileField(upload_to='materials', null=True)
#     by = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True)
#     level = models.ForeignKey(Level, related_name='material')
#
#     def by_name(self):
#         if self.by is not None:
#             return self.by.get_full_name
#         else:
#             return 'unknow'
#     by_name.short_description = _('upload by')
#     by_name.admin_order_field = 'by'
#
#     def file_size(self):
#         return filesizeformat(self.file.size)
#
#     def get_icon_html(self):
#         icon_cod = icon_type(self.file.name)
#         if icon_cod == 'img':
#             return format_html('<a href="{}"><i class="fa {}"></i></a>', self.file.url, 'fa-file-image-o')
#         else:
#             return format_html('<a href="{}"><i class="fa {}"></i></a>', self.file.url, icon_cod)
#     get_icon_html.short_description = _("File")
#
#     def __unicode__(self):
#         return self.name
#
#
class Room(models.Model):
    name = models.CharField(_("name"), max_length=30, unique=True, null=False,
                            blank=False)
    capacity = models.IntegerField(_("capacity"), default=0)
    equipments = models.TextField(_("equipments"), max_length=250)

    def __unicode__(self):
        return self.name


class TermReservationManager(models.Manager):
    def get_queryset(self):
        return super(TermReservationManager, self).get_queryset().\
            filter(start__isnull=False, start__gte=datetime.now())


class Term(models.Model):
    level = models.ForeignKey(Level)
    # teacher = models.ForeignKey(Teacher, related_name="teacher",
    #                             related_query_name="term")
    students = models.ManyToManyField(Student, related_query_name="term")
    room = models.ForeignKey(Room, default=1)

#     NO_SESSION = 1
#     RESERVE = 2
#     ACTIVE = 3
#     INACTIVE = 4
#     TERM_STATUS = {
#         NO_SESSION: 'No Session',
#         RESERVE: 'Reservation',
#         ACTIVE: 'Active',
#         INACTIVE: 'Inactive',
#     }
#     start = models.DateTimeField(null=True)
#     end = models.DateTimeField(null=True)
#     tuition = models.FloatField(null=True, blank=True)
#
#     objects = models.Manager()
#     reservation = TermReservationManager()
#
#     def __unicode__(self):
#         return self.level.name

#     def get_teacher_name(self):
#         return self.teacher.get_full_name
#     get_teacher_name.short_description = _('teacher')
#     get_teacher_name.admin_order_field = 'teacher'
#
#     def get_sessions_url(self):
#         return reverse('admin-panel:term_sessions', args=(self.pk,))
#
#     def sessions_icon(self):
#         return format_html('<a href="{}"><i class="fa fa-calendar"></i></a>', self.get_sessions_url())
#     sessions_icon.short_description = _('sessions')
#
#     def get_total_hour(self):
#         ret = 0
#         for s in self.sessions.all(): ret += s.duration
#         return ret
#
#     def no_of_sessions(self):
#         return self.sessions.all().count()
#
#     def no_of_students(self):
#         return self.students.all().count()
#
#     def get_start(self):
#         return self.sessions.all().order_by('start')[0]
#
#     def get_end(self):
#         return self.sessions.all().order_by('-start')[0]
#
#     def set_start_and_end(self):
#         self.start = self.get_start().start
#         self.end = self.get_end().end
#         self.save()
#
#     def get_exam(self):
#         return self.sessions.filter(is_exam=True)
#
#     def status(self):
#         if not self.start or not self.end:
#             return self.TERM_STATUS[self.NO_SESSION]
#         if now() < self.start:
#             return self.TERM_STATUS[self.RESERVE]
#         if now() < self.end:
#             return self.TERM_STATUS[self.ACTIVE]
#         else:
#             return self.TERM_STATUS[self.INACTIVE]
#
#     def get_duration(self):
#         start = self.get_start().date
#         end = self.get_end().date
#         return end - start
#
#     def get_supposed_income(self):
#         ret = 0
#         if self.tuition:
#             return self.students.all().count() * self.tuition
#         return ret
#
#     def get_supposed_outcome(self):
#         ret = 0
#         for s in self.sessions.all():
#             ret += s.outcome()
#         return ret
#
#     def get_supposed_profit(self):
#         si = self.get_supposed_income()
#         so = self.get_supposed_outcome()
#         return si - so
#
#     def save(self, *args, **kwargs):
#         if not self.tuition:
#             self.tuition = self.level.tuition
#         super(Term, self).save(*args, **kwargs)
#         # self.level.profit = self.level.supposed_profit()
#         # self.level.save()
#
#
# class Session(models.Model):
#     term = models.ForeignKey(Term, related_name="sessions", related_query_name="term", null=True)
#     start = models.DateTimeField()
#     end = models.DateTimeField()
#     absents = models.ManyToManyField(Student, related_query_name="session", null=True, blank=True)
#     is_exam = models.BooleanField(default=False)
#     canceled = models.BooleanField(default=False)
#
#     def save(self, *args, **kwargs):
#         super(Session, self).save(*args, **kwargs)
#         self.term.set_start_and_end()
#
#
# class StudentResume(models.Model):
#     student = models.ForeignKey(Student)
#     term = models.ForeignKey(Term)
#     reading = models.FloatField(validators=[MaxValueValidator(25)])
#     speaking = models.FloatField(validators=[MaxValueValidator(25)])
#     writing = models.FloatField(validators=[MaxValueValidator(25)])
#     class_activity = models.FloatField(validators=[MaxValueValidator(25)])
#     date = models.DateField(auto_now=True)
#
#     PASSED = 'passed'
#     FAILED = 'failed'
#     PASSED_CONDITIONALLY = 'passed conditionally'
#     TERM_STUDENT_STATUS = {
#         1: PASSED,
#         2: FAILED,
#         3: PASSED_CONDITIONALLY,
#     }
#
#     def total(self):
#         return self.reading + self.writing + self.speaking + self.class_activity
#
#     def student_name(self):
#         return self.student.get_full_name
#     student_name.short_description = _('Student name')
#
#     def resume_status(self):
#         total = self.total()
#         if total < 50:
#             return self.TERM_STUDENT_STATUS[2]
#         elif total < 70:
#             return self.TERM_STUDENT_STATUS[3]
#         else:
#             return self.TERM_STUDENT_STATUS[1]
#
#     class Meta:
#         unique_together = ("student", "term")

#
# class BaseLevel(models.Model):
#     edu = models.ForeignKey(Edu)
#     student = models.ForeignKey(Student)
#     level = models.ForeignKey(Level)
#     test_by = models.CharField(max_length=30, null=True, blank=True)
#     test_date = models.DateField(auto_now=True)
#
#     def student_name(self):
#         return self.student.get_full_name
#     student_name.short_description = _('Student name')
#
#     class Meta:
#         unique_together = ("edu", "student")