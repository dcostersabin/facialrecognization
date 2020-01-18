from django.db import models


class Employees(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255, unique=True)
    data_status = models.BooleanField(default=False)

