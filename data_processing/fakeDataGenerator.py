from user.models import Attendance, Employees
from datetime import date, timedelta, datetime
from django.utils.timezone import localtime
from random import randint

SERVER_START_DATE = datetime.strptime('1998/01/01', '%Y/%m/%d').date()
SERVER_END_DATE = datetime.strptime('2020/02/08', '%Y/%m/%d').date()


def date_iteration():
    for n in range(int(abs(SERVER_END_DATE - SERVER_START_DATE).days)):
        yield SERVER_START_DATE + timedelta(n)


def create_users():
    total_users = Employees.objects.all()
    # # fetch all users
    for users in total_users:
        for single_date in date_iteration():
            register_attendance = Attendance()
            register_attendance.entry_date = single_date
            register_attendance.exit_date = single_date
            register_attendance.entry_time = localtime().now().time()
            time_diff = randint(20000, 28800)
            time_added = localtime().now() + timedelta(0, time_diff)
            register_attendance.exit_time = time_added.time()
            register_attendance.user_id_id = users.id
            if randint(0, 1) == 1:
                register_attendance.save()
            else:
                pass
    return True
