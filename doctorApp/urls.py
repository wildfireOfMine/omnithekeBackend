from django.contrib import admin
from django.urls import path
from doctorApp import views

urlpatterns = [
    path("myDoctorProfile/", views.doctorProfileView.as_view()),
    path("myPatients/", views.myPatientsView.as_view()),
    path("addNewDoctors/<int:pk>", views.addNewDoctorView.as_view()),
    path("vaccines/", views.vaccinesView.as_view()),
    path("vaccines/<int:pk>", views.vaccinesPKView.as_view()),
    path("myAppointments/", views.appointmentsView.as_view()),
]