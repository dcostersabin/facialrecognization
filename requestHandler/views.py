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

    return render(request, 'attend.html',
                  {'name': user.name, 'employee_id': user.employee_id, 'id': user.id, 'status': 'check'})


@login_required
def home(request):
    if request.user.is_authenticated:
        employees = Employees.objects.order_by('-id')[:10]
        return render(request, "home.html", {'employees': employees})
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
        # return HttpResponse(file_path)
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
    user_path = user.name + '__id__' + str(user.id)
    no_files = len([name for name in os.listdir(path + '' + user_path) if
                    os.path.isfile(os.path.join(path + '' + user_path, name))])
    return render(request, "individualUser.html", {"data": user, "file": range(1, no_files)})


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
        messages.warning(request,"The Id Provided Doesnt Match")
        return HttpResponse(render(request, 'index.html'))
