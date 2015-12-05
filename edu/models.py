from django.core.validators import (MinValueValidator as Min,
                                    MaxValueValidator as Max)
from django.db import models
from django.conf import settings
import datetime
from itertools import groupby, chain
from django.template.defaultfilters import filesizeformat
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from usr.proxy_models import (Student, Teacher)
from edu.templatetags.file_icon import icon_type
from edu.managers import CourseReservationManager
from tinymce import models as tinymce_models



class Edu(models.Model):
    name = models.CharField(_("name"), max_length=30)
    language = models.CharField(_("language"), max_length=30,
                                choices=settings.EDU_LANGUAGES,
                                default=settings.EDU_DEFAULT_LANGUAGE)

    class Meta():
        verbose_name = "Education System"
        verbose_name_plural = "Education Systems"

    def __unicode__(self):
        return "{} {}".format(self.name, self.language)

    def no_of_grades(self):
        return Grade.objects.filter(edu=self).count()

    def no_of_courses(self):
        return Course.objects.filter(grade__edu=self).count()

    def no_of_sessions(self):
        return Session.objects.filter(course__grade__edu=self).count()


# def grade_of_student(self, stu):
#     resumes = stu.studentresume_set.filter(course__grade__edu=self).order_by('-date')
#     last_grade = resumes[0].course.grade
#     per_last_grade = resumes[1].course.grade
#     base_grade = stu.basegrade_set.get(edu=self).grade
#     i = last_grade.index + 1
#     try:
#         next_grade = self.grade_set.get(index=i)
#     except:
#         next_grade = None
#     if not last_grade and not base_grade:
#         return self.grade_set.get(index=1)
#     if base_grade and not last_grade:
#         return base_grade
#     if base_grade and last_grade and base_grade.index > last_grade.index:
#         return base_grade
#     if resumes[0].resume_status == StudentResume.PASSED:
#         return next_grade
#     if resumes[1].resume_status == StudentResume.PASSED_CONDITIONALLY:
#         return per_last_grade
#     if resumes[0].resume_status == StudentResume.PASSED_CONDITIONALLY:
#         return next_grade
#     if resumes[0].resume_status == StudentResume.FAILED:
#         return last_grade


class Semester(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    start = models.DateField()
    end = models.DateField()

    @classmethod
    def get_current(cls):
        return cls.objects.filter(start__lte=datetime.date.today(),
                                  end__gte=datetime.date.today())[0]

    def get_events(self, course_set=False):
        # Create a dictionary of months in the semester that contains
        #  defaultdicts of lists
        start = datetime.datetime.combine(self.start, datetime.time(0, 0))
        end = datetime.datetime.combine(self.end, datetime.time(0, 0))

        occurrences = []

        if not course_set:
            course_set = self.course_set.all()

        # Gather all the occurences
        for course in course_set:
            for event in course.schedule.all():
                occurrences.append([(single_occurence, event)
                                    for single_occurence in
                                    event.recurrences.occurrences(
                                        dtstart=start, dtend=end)])

        months = dict([(month, list(events)) for month, events in
                       groupby(chain(*occurrences), lambda a: a[0].month)])

        for month, e in months.items():
            months[month] = dict([(day, list(events)) for day, events in
                                  groupby(e, lambda a: a[0].day)])

        return months

    @classmethod
    def get_current_events(cls):
        return cls.get_current().get_events()

    def active(self):
        return self.start <= datetime.date.today() and self.end >= datetime.date.today()

    def save(self, *args, **kwargs):
        # if self.start > self.end:
        #   raise ValueError, "Start date must be before end date."
        return super(Semester, self).save(*args, **kwargs)

    @property
    def is_future(self):
        '''
        Checks if the start date is in the future
        '''
        return self.start > datetime.date.today()

    def get_next(self):
        '''
        Try to return the semester after this one.
        '''
        semesters = Semester.objects.filter(start__gt=self.end).order_by(
            '-start')
        if len(semesters) > 0:
            return semesters[0]
        else:
            raise Semester.DoesNotExist

    def __unicode__(self):
        return "%s %s" % (self.name, self.year)


class Grade(models.Model):
    edu = models.CharField(_("education system"), max_length=30)
    name = models.CharField(_("name"), max_length=30)
    index = models.PositiveSmallIntegerField(_("index"))
    tuition = models.FloatField(_("tuition"), null=True, blank=True)
    capacity = models.PositiveSmallIntegerField(_("capacity"), null=True,
                                                blank=True)

    def no_of_courses(self):
        return Course.objects.filter(grade=self).count()

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("index", "edu")


class Course(models.Model):
    grade = models.ForeignKey(Grade)
    number = models.CharField(max_length=10)
    title = models.CharField(max_length=200)

    teacher = models.ForeignKey(Teacher, related_name="teacher",
                                related_query_name="course")
    teaching_assistants = models.ManyToManyField(
        Teacher, related_name=_('assistant'))

    members = models.ManyToManyField(Student, related_query_name="course")

    semester = models.ForeignKey(Semester)
    exam = models.DateTimeField(null=True)
    location = models.CharField(null=True, max_length=150)

    private = models.BooleanField(default=False, blank=True)

    objects = models.Manager()
    reservation = CourseReservationManager()

    def __unicode__(self):
        return self.grade.name

    def get_teacher_name(self):
        return self.teacher.get_full_name

    get_teacher_name.short_description = _('teacher')
    get_teacher_name.admin_order_field = 'teacher'


# def get_sessions_url(self):
#         return reverse('admin-panel:course_sessions', args=(self.pk,))
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
#             return self.COURSE_STATUS[self.NO_SESSION]
#         if now() < self.start:
#             return self.COURSE_STATUS[self.RESERVE]
#         if now() < self.end:
#             return self.COURSE_STATUS[self.ACTIVE]
#         else:
#             return self.COURSE_STATUS[self.INACTIVE]
#
#     def get_duration(self):
#         start = self.get_start().date
#         end = self.get_end().date
#         return end - start

#
#     def save(self, *args, **kwargs):
#         if not self.tuition:
#             self.tuition = self.grade.tuition
#         super(Course, self).save(*args, **kwargs)
#         # self.grade.profit = self.grade.supposed_profit()
#         # self.grade.save()


class Session(models.Model):
    course = models.ForeignKey(Course, related_name="sessions",
                               related_query_name="course", null=True)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    location = models.CharField(null=True, max_length=150)

    # absents = models.ManyToManyField(Student, related_query_name="session",
    #                                  blank=True)
    # canceled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Session, self).save(*args, **kwargs)
        # self.course.set_start_and_end()


class Transcript(models.Model):
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    reading = models.PositiveSmallIntegerField(validators=[Max(25)])
    speaking = models.PositiveSmallIntegerField(validators=[Max(25)])
    writing = models.PositiveSmallIntegerField(validators=[Max(25)])
    class_activity = models.PositiveSmallIntegerField(validators=[Max(25)])

    # I should make sure about auto_now argument exact behavior.
    submit_date = models.DateTimeField(auto_now=True)

    def total(self):
        return self.reading + self.writing + self.speaking + self.class_activity

    def student_name(self):
        return self.student.get_full_name

    def status(self):
        total = self.total()
        if total < settings.TRANSCRIPT_FAIL_VALUE:
            return settings.TRANSCRIPT_STATUS_FAIL
        elif total > settings.TRANSCRIPT_PASS_VALUE:
            return settings.TRANSCRIPT_STATUS_PASS
        else:
            return settings.TRANSCRIPT_STATUS_CONDITIONAL

    class Meta:
        unique_together = ("student", "course")

    student_name.short_description = _('Student name')


class Placement(models.Model):
    student = models.ForeignKey(Student)
    grade = models.ForeignKey(Grade)
    examiner = models.ForeignKey(Teacher, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def student_name(self):
        return self.student.get_full_name

    student_name.short_description = _('Student name')
    #
    # class Meta:
    #     unique_together = ("edu", "student")


# class Assignment(models.Model):
#     course = models.ForeignKey(Course)
#     title = models.CharField(max_length=200)
#     description = tinymce_models.HTMLField()
#     due_date = models.DateField(null=True)
#
#     def __unicode__(self):
#         return self.title
#
#
# class AssignmentSubmission(models.Model):
#     # if settings.NONREL:
#     #     users = fields.ListField(ForeignKey(User, related_name = 'submitters'))
#     # else:
#     users = models.ManyToManyField(Student, related_name='submitters')
#
#     assignment = models.ForeignKey(Assignment)
#     link = models.URLField(blank=True)
#     file = models.FileField(upload_to='photos/%Y/%m/%d', blank=True)
#     notes = models.TextField(blank=True)
#
#     submitted = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now_add=True, auto_now=True)
#
#     def late(self):
#         return self.submitted.date() > self.assignment.due_date
#
#     def __unicode__(self):
#         if self.link:
#             return self.link
#         elif self.file:
#             return self.file.name


class Resource(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True)
    file = models.FileField(upload_to='resources/%Y/%m/%d', blank=True)
    upload_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                  blank=True)
    description = tinymce_models.HTMLField()

    def __unicode__(self):
        return self.title

# class Material(models.Model):
#     name = models.CharField(max_length=254, unique=True)
#     file = models.FileField(upload_to='materials', null=True)
#     by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
#     grade = models.ForeignKey(Grade, related_name='material')
#
#     def by_name(self):
#         if self.by is not None:
#             return self.by.get_full_name
#         else:
#             return 'unknow'
#
#     def file_size(self):
#         return filesizeformat(self.file.size)
#
#     def get_icon_html(self):
#         icon_cod = icon_type(self.file.name)
#         if icon_cod == 'img':
#             return format_html('<a href="{}"><i class="fa {}"></i></a>',
#                                self.file.url, 'fa-file-image-o')
#         else:
#             return format_html('<a href="{}"><i class="fa {}"></i></a>',
#                                self.file.url, icon_cod)
#
#     get_icon_html.short_description = _("File")
#     by_name.short_description = _('upload by')
#     by_name.admin_order_field = 'by'
#
#     def __unicode__(self):
#         return self.name
#

class Room(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    capacity = models.PositiveSmallIntegerField(null=True)
    equipments = models.TextField(max_length=250)

    def __unicode__(self):
        return self.name
