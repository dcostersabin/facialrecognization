from django.db import models
from user.models import Attendance, Employees


class FirstFilter(models.Model):
    user_id = models.ForeignKey(Attendance, on_delete=models.CASCADE, null=False)
    day = models.CharField(max_length=255, null=True)
    hours_worked = models.FloatField(default=0)


