from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from usersApp.serializers import TokenSerializer, DoctorSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from usersApp.models import Doctor

# Create your views here.

class ObtenerToken(TokenObtainPairView):

    serializer_class = TokenSerializer

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