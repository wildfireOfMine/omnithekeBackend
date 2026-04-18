from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from adminApp import views

urlpatterns = [
    path("", views.adminView.as_view()),
    path("<int:pk>/", views.adminView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
]