from django.forms import ModelForm

from user.models import Employees


class EmployeeAddingForm(ModelForm):
    class Meta:
        model = Employees
        fields = ['name', 'employee_id', 'department', 'post']
