from django.db import models
from user.models import Attendance, Employees


class FirstFilter(models.Model):
    user_id = models.ForeignKey(Employees, on_delete=models.CASCADE, null=False)
    day = models.CharField(max_length=255, null=True)
    hours_worked = models.FloatField(default=0)
    entry_date = models.DateField(blank=True)
    entry_time = models.TimeField(blank=True)


class TableRecords(models.Model):
    table_name = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now_add=True)


class UserDailyAttendance(models.Model):
    user_id = models.ForeignKey(Employees, on_delete=models.CASCADE, null=False)
    hour_worked = models.FloatField(default=0)
    whichDay = models.BigIntegerField(blank=False)


class NeuralNetworkRecord(models.Model):
    use_id = models.ForeignKey(Employees,on_delete=models.CASCADE,null=False)
    trained_data = models.TextField
    actual_data = models.TextField
    predicted_data = models.TextField