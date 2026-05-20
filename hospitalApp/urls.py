from django.contrib import admin
from django.urls import path
from hospitalApp import views

urlpatterns = [
    path("hospital/", views.hospitalView.as_view()),
    path("hospital/<int:pk>", views.hospitalPKView.as_view()),
    path("department/", views.departmentView.as_view()),
    path("department/<int:pk>", views.departmentPKView.as_view()),
    path("floor/", views.floorView.as_view()),
    path("floor/<int:pk>", views.floorPKView.as_view()),
    path("room/", views.roomView.as_view()),
    path("room/<int:pk>", views.roomPKView.as_view()),
    path("administrator/", views.administratorView.as_view()),
    path("administrator/<int:pk>", views.administratorPKView.as_view()),
]