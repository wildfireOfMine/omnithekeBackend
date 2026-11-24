from django.urls import path
from historyApp import views

urlpatterns = [
    path('misConsultas/', views.todasConsultasPacienteView.as_view()),
    path('misConsultasDoctor/', views.todasConsultasDoctorView.as_view()),
    path('miConsulta/<int:pk>/', views.consultaView.as_view()),
    path('consultaGet/<int:pk>/', views.consultaGetView.as_view()),
    path('nuevaConsulta/', views.nuevaConsultaView.as_view()),
    path('consultaPatch/<int:pk>/', views.consultaPatchView.as_view()),
]