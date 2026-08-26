from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from usersApp import views

urlpatterns = [

    path('login/', views.ObtenerToken.as_view()),
    path('registrarse/', views.registrarseView.as_view()),
    path('todosDoctores/', views.todosDoctoresView.as_view()),
    path('especialidades/', views.todasEspecialidades.as_view()),
]