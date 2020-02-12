from django.shortcuts import render
from datetime import datetime, time, timedelta
from user.models import Attendance, Employees
from machineLearning.models import FirstFilter
from machineLearning.models import TableRecords, UserDailyAttendance
from data_processing.fakeDataGenerator import date_iteration
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

SERVER_START_DATE = datetime.strptime('1998/01/01', '%Y/%m/%d').date()
SERVER_END_DATE = datetime.strptime('2020/02/12', '%Y/%m/%d').date()


def sort_data_to_first_filter():
    if FirstFilter.objects.all().delete():
        all_records = Attendance.objects.all()
        for data in all_records:
            sort = FirstFilter()
            sort.user_id_id = data.user_id_id
            sort.day = datetime.strftime(data.entry_date, '%w')
            entry = datetime.strptime(str(data.entry_date) + '/' + str(data.entry_time), '%Y-%m-%d/%H:%M:%S.%f')
            if data.exit_date:
                exited = datetime.strptime(str(data.exit_date) + '/' + str(data.exit_time), '%Y-%m-%d/%H:%M:%S.%f')
                diff = (exited - entry) / (60 * 60)
                if diff == 0:
                    pass
                diff = str(diff)
                diff = diff.split(':', 3)
            else:
                pass
            sort.hours_worked = diff[2]
            sort.entry_date = data.entry_date
            sort.entry_time = data.entry_time
            sort.save()
        # check if the table exists
        check = TableRecords.objects.filter(table_name='firstFilter').first()
        if check:
            check.update_at = datetime.now()
            check.save()
            return True

        else:
            new = TableRecords()
            new.table_name = 'firstFilter'
            new.save()
            return True
        return True
    else:
        return False


def sort_data_to_days():
    days = list()
    for i in range(0, 7):
        no =FirstFilter.objects.filter(day=i).count()
        days.append(no)

    return days


def user_daily_attendance():
    if UserDailyAttendance.objects.all().delete():
        users_all = Employees.objects.all()
        for user in users_all:
            counter = 0
            for single_date in date_iteration():
                counter += 1
                attendance_for_day = FirstFilter.objects.filter(user_id_id=user.employee_id,
                                                                entry_date=single_date).first()

                if attendance_for_day:
                    new_record = UserDailyAttendance()
                    new_record.user_id_id = user.employee_id
                    new_record.whichDay = counter
                    new_record.hour_worked = attendance_for_day.hours_worked
                    new_record.save()
                else:
                    pass
        return True
    else:
        return False


def users_hour_prediction(user):
    check_user = Employees.objects.filter(employee_id=user)
    if check_user:
        actual = []
        predicted = []
        users_days = UserDailyAttendance.objects.filter(user_id_id=user).order_by('-whichDay')
        X = list()
        Y = list()
        for users in users_days:
            x = list()
            y = list()
            x.append(users.whichDay)
            y.append(users.hour_worked)
            X.append(x)
            Y.append(y)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=(1 / 3), random_state=1)
        regressor = LinearRegression()
        regressor.fit(X_train, Y_train)
        y_predict = regressor.predict(X_test)
        for x in X_test:
            actual.append([x[0], 0])
        counter = 0
        for y in Y_test:
            actual[counter][1] = y[0]
            counter += 1
        for x in X_test:
            predicted.append([x[0], 0])
        counter = 0
        for y in y_predict:
            predicted[counter][1] = y[0]
            counter += 1

        for i in range(0, len(y_predict)):
            print("actual:", Y_test[i], "calculated", y_predict[i])

        # //prediction for next 20 days
        future = list()
        for i in range(len(users_days), len(users_days) + 20):
            future.append(regressor.predict([[i]]))

        return [predicted, actual, future]

    else:
        return False
