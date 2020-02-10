from django.shortcuts import render
from datetime import datetime, time
from user.models import Attendance
from machineLearning.models import FirstFilter


def sort_data_to_first_filter():
    all_records = Attendance.objects.all()
    for data in all_records:
        sort = FirstFilter()
        sort.user_id_id = data.id
        sort.day = datetime.strftime(data.entry_date, '%w')
        entry = datetime.strptime(str(data.entry_date) + '/' + str(data.entry_time), '%Y-%m-%d/%H:%M:%S.%f')
        if data.exit_date:
            exited = datetime.strptime(str(data.exit_date) + '/' + str(data.exit_time), '%Y-%m-%d/%H:%M:%S.%f')
            diff = (exited - entry) / (60 * 60)
            diff = str(diff)
            diff = diff.split(':', 3)
        else:
            diff = 0
        sort.hours_worked = diff[2]
        sort.save()
    return True


def sort_data_to_days():
    days = {}
    for i in range(0, 7):
        days[str(i)] = FirstFilter.objects.filter(day=i).count()

    return days
