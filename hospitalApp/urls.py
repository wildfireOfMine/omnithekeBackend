from django.contrib import admin
from django.urls import path
from hospitalApp import views

urlpatterns = [
    path("hospital/", views.hospitalView.as_view()),
    path("hospital/<int:pk>", views.hospitalPKView.as_view()),
    path("department/", views.departmentView.as_view()),
    path("department/<int:pk>", views.departmentPKView.as_view()),
    path("administrator/", views.administratorView.as_view()),
    path("administrator/<int:pk>", views.administratorPKView.as_view()),
]