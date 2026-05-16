from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from authApp import views

urlpatterns = [
    path('register/', views.registerView.as_view()),
    path('login/', views.ObtainToken.as_view()),
    path('users/', views.userView.as_view()),
    path('users/<int:pk>', views.userViewPK.as_view()),
]