from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from usersApp.serializers import TokenSerializer

# Create your views here.


class ObtainToken(TokenObtainPairView):

    serializer_class = TokenSerializer