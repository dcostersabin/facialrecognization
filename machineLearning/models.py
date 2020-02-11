from django.db import models
from user.models import Attendance, Employees


class FirstFilter(models.Model):
    user_id = models.ForeignKey(Attendance, on_delete=models.CASCADE, null=False)
    day = models.CharField(max_length=255, null=True)
    hours_worked = models.FloatField(default=0)


class TableRecords(models.Model):
    table_name = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now_add=True)


class UserDailyAttendance(models.Model):
    user_id = models.ForeignKey(Employees, on_delete=models.CASCADE, null=False)
    hour_worked = models.FloatField(default=0)
    whichDay = models.BigIntegerField(blank=False)
