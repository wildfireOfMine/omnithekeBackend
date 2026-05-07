from django.contrib import admin
from django.urls import path
from doctorApp import views

urlpatterns = [
    path("myDoctorProfile/", views.doctorProfileView.as_view()),
]