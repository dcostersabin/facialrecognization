from django.db import models


class Employees(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255, unique=True)
    data_status = models.BooleanField(default=False)


class Attendance(models.Model):
    user_id = models.ForeignKey(Employees, on_delete=models.CASCADE, null=False)
    entry_date = models.DateTimeField(blank=True)
    exit_date = models.DateTimeField(blank=True)
