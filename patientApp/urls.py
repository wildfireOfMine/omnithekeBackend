from django.contrib import admin
from django.urls import path
from patientApp import views

urlpatterns = [
    path("myPatientProfile/", views.myProfile.as_view()),
]