from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from adminApp import views

urlpatterns = [
    path("", views.test.as_view()),
    path('login/', TokenObtainPairView.as_view()),
]