from django.contrib import admin
from django.urls import path
from patientApp import views

urlpatterns = [
    path("myPatientProfile/", views.myProfileView.as_view()),
]