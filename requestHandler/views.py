import os

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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = BASE_DIR + '/static/dataset/'


def index(request):
    return HttpResponse(render(request, "index.html"), )


def capture(request):
    if data_collection.capture_image((request.POST['id']), 0):
        return HttpResponse("Data Has Been SuccessFully Collected")
    else:
        return HttpResponse("not created")


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
    return HttpResponse(name)


def home(request):
    employees = Employees.objects.order_by('-id')[:10]
    return render(request, "home.html", {'employees': employees})


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
        return HttpResponse("Data Has Been SuccessFully Collected")
    else:
        return HttpResponse("not created")


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
