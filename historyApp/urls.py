from django.urls import path
from historyApp import views

urlpatterns = [
    path('misConsultas/', views.todasConsultasPacienteView.as_view()),
]