from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from doctorApp.serializers import AdministratorSerializer, DoctorSerializer, PatientSerializer
from adminApp.models import Administrator
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class doctorProfileView(APIView):
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        summary="GET your Doctor Profile",
        description="Get your doctor profile with all your attributes",
        responses=DoctorSerializer,
    )
    def get(self, request):
        doctor = request.user.doctor
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)