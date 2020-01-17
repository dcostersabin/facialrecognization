from django.urls import path
from requestHandler import views


urlpatterns = [
    path('', views.index, name="index"),
    path('capture/', views.capture, name="capture"),
    path('train/',views.train_data, name="train"),
    path('recognize/',views.rec,name="recognize"),
    path('hello/',views.HelloView.as_view(),name="hello"),
    path('home/',views.home,name="home"),

]
