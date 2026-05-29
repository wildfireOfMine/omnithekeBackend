from django.contrib import admin
from django.urls import path
from officeApp import views

urlpatterns = [
    path("office/", views.officeView.as_view()),
    path("office/<int:pk>", views.officePKView.as_view()),
    path("department/", views.departmentView.as_view()),
    path("department/<int:pk>", views.departmentPKView.as_view()),
    path("administrator/", views.administratorView.as_view()),
    path("administrator/<int:pk>", views.administratorPKView.as_view()),
]