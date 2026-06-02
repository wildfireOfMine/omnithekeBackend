from django.contrib import admin
from django.urls import path
from patientApp import views

urlpatterns = [
    path("myPatientProfile/", views.myProfileView.as_view()),
    path("myDoctors/", views.myDoctorsView.as_view()),
    path("myIncidents/", views.myIncidentsView.as_view()),
    path("myReports/", views.myReportsView.as_view()),
    path("messages/", views.messagesView.as_view()),
    path("appointments/", views.appointmentsView.as_view()),
    path("appointments/<int:pk>/", views.appointmentsPKView.as_view()),
]