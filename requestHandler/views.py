from django.shortcuts import render
from django.http import HttpResponse
from recognition import data_collection
from recognition import train
from recognition import recognize


def index(request):
    return render(request, template_name='home.html')


def capture(request):
    if data_collection.create_dir(str(request.POST['name'])):
        if data_collection.capture_image(str(request.POST['name'])):
            return HttpResponse("Data Has Been SuccessFully Collected")

    else:
        return HttpResponse("not created")


def train_data(request):
    status = train.train()
    if status:
        return HttpResponse("Training Success")
    else:
        return HttpResponse("Failed To Train")


def rec(request):
   name =  recognize.recognize()
   return HttpResponse(name)
