from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from authApp import views

urlpatterns = [
    path('register/', views.registerView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
]