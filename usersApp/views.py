from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from usersApp.serializers import TokenSerializer, DoctorSerializer, RegistrarseSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from usersApp.models import Doctor

# Create your views here.

class ObtenerToken(TokenObtainPairView):

    serializer_class = TokenSerializer

class registrarseView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="POST de un Usuario",
        description="Registra un usuario en la BBDD",
        request=RegistrarseSerializer,
        responses=RegistrarseSerializer(many=True),
    )
    def post(self, request):
        serializador = RegistrarseSerializer(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)

class todosDoctoresView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary="GET de Doctores",
        description="GET de todos los Doctores en la BBDD",
        request=DoctorSerializer,
        responses=DoctorSerializer(many=True),
    )
    def get(self, request):
        doctores = Doctor.objects.all()
        serializador = DoctorSerializer(doctores, many=True)
        return Response(serializador.data)