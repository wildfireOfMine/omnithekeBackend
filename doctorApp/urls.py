from django.contrib import admin
from django.urls import path
from doctorApp import views

urlpatterns = [
    path("myDoctorProfile/", views.doctorProfileView.as_view()),
    path("myPatients/", views.myPatientsView.as_view()),
    path("myAppointments/", views.appointmentsView.as_view()),
    path("myAppointments/<int:pk>/", views.appointmentsPKView.as_view()),
    path("myIncidents/", views.incidentsView.as_view()),
    path("myIncidents/<int:pk>/", views.incidentsViewPK.as_view()),
    path("myReports/", views.reportsView.as_view()),
    path("myReports/<int:pk>/", views.reportsPKView.as_view()),
    path("incidents/<int:pk>/", views.patientIncidentsView.as_view()),
    path("patient/<int:pk>/", views.patientViewPK.as_view()),
]