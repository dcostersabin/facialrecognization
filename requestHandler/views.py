import os
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from recognition import data_collection
from recognition import train
from recognition import recognize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from requestHandler.add_user_form import EmployeeAddingForm
from django.contrib import messages
from user.models import Employees
from user.models import Attendance
from django.contrib.auth.decorators import login_required
from requestHandler.renderPdf import render_to_pdf
from rest_framework.decorators import api_view
from data_processing.fakeDataGenerator import create_users
from machineLearning.views import sort_data_to_first_filter, sort_data_to_days

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = BASE_DIR + '/static/dataset/'


def index(request):
    return HttpResponse(render(request, "index.html"), )


def capture(request):
    if data_collection.capture_image((request.POST['id']), 0):
        messages.success(request, "Data Has Been Collected Successfully")
        return redirect('home')
    else:
        messages.success(request, "Data Creation Failed")
        return redirect('home')


def train_data(request):
    status = train.train()
    if status:
        messages.success(request, "The Machine Was Trained Successfully")
        return redirect('home')
    else:
        messages.warning(request, "The Machine Failed To  Train")
        return redirect('home')


def rec(request):
    name = recognize.recognize()
    temp_id = name.split("__id__", 1)
    user = Employees.objects.filter(id=temp_id[1]).get()
    user_path = user.name + '__id__' + str(user.id)
    if Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id,
                                 exit_date=datetime.now().date()).exists():
        user_current_data = Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id).get()
        return render(request, 'attend.html',
                      {'name': user.name, 'employee_id': user.employee_id, 'id': user.id, 'status': 'check',
                       'attendance': True, 'entry_date': user_current_data.entry_date,
                       'entry_time': user_current_data.entry_time, 'complete': True,
                       'exit_time': user_current_data.exit_time})
    elif Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id).exists():
        user_current_data = Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id).get()
        return render(request, 'attend.html',
                      {'name': user.name, 'employee_id': user.employee_id, 'id': user.id, 'status': 'check',
                       'attendance': True, 'entry_date': user_current_data.entry_date,
                       'entry_time': user_current_data.entry_time, 'complete': False, })
    else:
        return render(request, 'attend.html',
                      {'name': user.name, 'employee_id': user.employee_id, 'id': user.id, 'status': 'check',
                       'attendance': False, 'complete': False})


@login_required
def home(request):
    if request.user.is_authenticated:
        employees = Employees.objects.order_by('-id')[:10]
        today_count = Attendance.objects.filter(entry_date=datetime.now().date()).count()
        today = Attendance.objects.filter(entry_date=datetime.now().date())[:10]
        return render(request, "home.html", {'employees': employees, 'today': today, 'todays_count': today_count,
                                             'employees_count': employees.count()})
    else:
        return render(request, 'index.html')


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'hello world'}
        return Response(content)


def add_user(request):
    user = EmployeeAddingForm(request.POST)
    if user.is_valid():
        new = user.save()
        file_path = new.name + '__id__' + str(new.id)
        data_collection.create_dir(file_path)
        if os.path.isdir(path + '' + file_path):
            messages.success(request, f'New User Added Now You Can Add Data')
            return redirect('home')
        else:
            messages.info(request, f'Failed To Create User Enter Valid Data')
            return redirect('home')

    else:
        messages.warning(request, f'Failed To Create User Enter Valid Data')
        return redirect('home')


def show_users(request):
    employees = Employees.objects.all().order_by('-id')
    return render(request, 'showusers.html', {'employees': employees})


def add_more_data(request):
    if data_collection.capture_image(request.POST['id'], 1):
        messages.success(request, "New Data Collected Successfully")
        return redirect('home')
    else:
        messages.warning(request, "Failed To Initialized Data")
        return redirect('home')


def admin_test(request):
    name = recognize.recognize()
    temp_id = name.split("__id__", 1)
    user = Employees.objects.filter(id=temp_id[1]).get()
    user_path = user.name + '__id__' + str(user.id)
    no_files = len([name for name in os.listdir(path + '' + user_path) if
                    os.path.isfile(os.path.join(path + '' + user_path, name))])
    return render(request, "individualUser.html", {"data": user, "file": range(1, no_files)})


def view_profile(request):
    user = Employees.objects.filter(id=request.POST['user_id']).get()
    total_attendance = Attendance.objects.filter(user_id=user.id).order_by('-entry_date')
    user_path = user.name + '__id__' + str(user.id)
    no_files = len([name for name in os.listdir(path + '' + user_path) if
                    os.path.isfile(os.path.join(path + '' + user_path, name))])
    return render(request, "individualUser.html",
                  {"data": user, "file": range(1, no_files), 'attendance': total_attendance})


def search(request):
    try:
        user = Employees.objects.filter(employee_id=request.POST['user_id']).get()
        user_path = user.name + '__id__' + str(user.id)
        no_files = len([name for name in os.listdir(path + '' + user_path) if
                        os.path.isfile(os.path.join(path + '' + user_path, name))])
        return render(request, 'individualUser.html', {'data': user, 'file': range(1, no_files)})
    except ObjectDoesNotExist as e:
        messages.warning(request, "Please Enter A Valid Data")
        return redirect('home')


def attend(request):
    # return HttpResponse(datetime.now().date())

    if Employees.objects.filter(id=request.POST['id']).exists():
        user = Employees.objects.filter(id=request.POST['id']).get()
        check = Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id).exists()
        if not check:
            new = Attendance()
            new.user_id_id = user.id
            new.entry_date = datetime.now().date()
            new.entry_time = datetime.now().time()
            new.save()
            messages.success(request, "Recorded Entry For User " + user.name)
            return redirect('index')

        else:
            update = Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id).get()
            update.exit_date = datetime.now().date()
            update.exit_time = datetime.now().time()
            update.save()
            messages.success(request, "Recorded Exit For User " + user.name)
            return redirect('index')

    else:
        messages.warning(request, "The Id Provided Doesnt Match")
        return HttpResponse(render(request, 'index.html'))


def report(request):
    start = request.GET.get('start', False)
    ends = request.GET.get('end', False)
    if not (start and ends):
        records = list()
        start = datetime.now().date()
        ends = datetime.now().date()
        all_employees = Employees.objects.all()
        for emp in all_employees:
            records_available = Attendance.objects.filter(entry_date__range=[start, ends], user_id=emp.id).order_by(
                '-entry_date')
            if len(records_available) > 0:
                total = len(records_available)
                records_available = records_available[0]
            else:
                total = len(records_available)
            records.append({'detail': emp, 'record': records_available,
                            'total_record': total})
        return render(request, 'report.html', {
            'start': start, 'ends': ends, 'records': records,
            'days': abs((ends - start).days)
        })
    else:
        start = datetime.strptime(request.GET['start'], '%Y-%m-%d')
        ends = datetime.strptime(request.GET['end'], '%Y-%m-%d')
        if ends > start and (ends <= datetime.now()):
            records = list()
            all_employees = Employees.objects.all()
            for emp in all_employees:
                records_available = Attendance.objects.filter(entry_date__range=[start, ends], user_id=emp.id).order_by(
                    '-entry_date')
                if len(records_available) > 0:
                    total = len(records_available)
                    records_available = records_available[0]
                else:
                    total = len(records_available)
                records.append({'detail': emp, 'record': records_available,
                                'total_record': total})

            return render(request, 'report.html', {
                'start': request.GET['start'], 'ends': request.GET['end'], 'records': records,
                'days': abs((ends - start).days)
            })
        else:
            messages.warning(request, "Please Enter A Valid Date")
            return render(request, 'report.html', {
                'start': start, 'ends': ends,
            })


def charts(request):
    days = sort_data_to_days()
    return render(request, 'charts.html', {'days': days})


def download_pdf(request):
    try:
        start = datetime.strptime(request.GET['start'], '%Y-%m-%d')
        ends = datetime.strptime(request.GET['end'], '%Y-%m-%d')
        if ends > start and (ends <= datetime.now()):
            records = list()
            all_employees = Employees.objects.all()
            for emp in all_employees:
                records_available = Attendance.objects.filter(entry_date__range=[start, ends], user_id=emp.id)
                if len(records_available) > 0:
                    total = len(records_available)
                    records_available = records_available[0]
                else:
                    total = len(records_available)
                records.append({'detail': emp, 'record': records_available,
                                'total_record': total})

            pdf = render_to_pdf('report_pdf.html', {'records': records, 'start': start, 'end': ends})
            return HttpResponse(pdf, content_type='application/pdf')
    except Exception as e:
        messages.warning(request, "Cant Generate Report For A Single Day")
        return redirect('report')


@api_view(['GET'])
def chart_data(request):
    days = sort_data_to_days()
    return Response((days))
