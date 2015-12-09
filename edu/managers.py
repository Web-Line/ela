from datetime import datetime
from django.db import models


class CourseReservationManager(models.Manager):
    def get_queryset(self):
        return super(CourseReservationManager, self).get_queryset().filter(
            start__isnull=False, start__gte=datetime.now())
