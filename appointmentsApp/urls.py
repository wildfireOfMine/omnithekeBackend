from django.contrib import admin
from django.urls import path
from appointmentsApp import views

urlpatterns = [
    path('misCitas/', views.todasCitasPacienteView.as_view()),
]