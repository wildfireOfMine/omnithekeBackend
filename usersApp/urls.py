from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from usersApp import views

urlpatterns = [
    path('login/', views.ObtenerToken.as_view()),
    path('registrarse/', views.registrarseView.as_view()),
    path('confirmarCuenta/', views.confirmarCuentaView.as_view()),
    path('solicitarRecuperacion/', views.solicitarRecuperacionView.as_view()),
    path('restablecerContrasena/', views.restablecerContrasenaView.as_view()),
    path('todosDoctores/', views.todosDoctoresView.as_view()),
    path('especialidades/', views.todasEspecialidadesView.as_view()),
    path('especialidadesList/', views.todasEspecialidadesListView.as_view()),
    path('especialidadPost/', views.especialidadPostView.as_view()),
    path('aseguradoras/', views.todasAseguradorasView.as_view()),
    path('aseguradorasList/', views.todasAseguradorasListView.as_view()),
    path('recepcionistasList/', views.todosRecepcionistasListView.as_view()),
    path('doctor/<int:pk>/', views.doctorView.as_view()),
]