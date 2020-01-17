from django.http import HttpResponse
from django.shortcuts import render
from recognition import data_collection
from recognition import train
from recognition import recognize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def index(request):
    return HttpResponse(render(request,"index.html"))


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
    name = recognize.recognize()
    return HttpResponse(name)


def home(request):
    return HttpResponse(render(request, "home.html"))


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'hello world'}
        return Response(content)
