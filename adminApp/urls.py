from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from adminApp import views

urlpatterns = [
    path("doctor/", views.doctorView.as_view()),
    path("doctor/<int:pk>/", views.doctorViewPK.as_view()),
    path("patient/", views.patientView.as_view()),
    path("patient/<int:pk>/", views.patientViewPK.as_view()),
    path("myProfile/", views.administratorView.as_view())
]