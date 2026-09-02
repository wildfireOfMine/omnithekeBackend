from django.contrib import admin
from django.urls import path
from appointmentsApp import views

urlpatterns = [
    path('misCitas/', views.todasCitasPacienteView.as_view()),
    path('horariosDisponibles/<int:pk>/', views.horariosView.as_view()),
    path('horaDisponible/<int:pk>/<str:fecha>/', views.horasDisponiblesView.as_view()),
    path('nuevaCita/', views.crearCitaView.as_view()),
]