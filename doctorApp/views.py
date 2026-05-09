from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from doctorApp.serializers import AdministratorSerializer, DoctorSerializer, PatientSerializer
from adminApp.models import Administrator
from doctorApp.models import Doctor
from patientApp.models import Patient
from rest_framework.response import Response
from rest_framework import permissions, status
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
    
    @extend_schema(
        summary="PUT your Doctor Profile",
        description="Put your own doctor profile",
        request=DoctorSerializer,
        responses={201: DoctorSerializer, 400: dict},
    )
    def put(self, request):
        doctor = request.user.doctor
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class myPatientsView(APIView):
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        summary="GET your Patients",
        description="Get a list of your patients as a doctor",
        responses=PatientSerializer,
    )
    def get(self, request):
        doctor = request.user.doctor
        relatedPatients = Patient.objects.filter(doctors=doctor.pk)
        serializer = PatientSerializer(relatedPatients, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="POST a new Patient",
        description="Post a new patient in the database",
        request=PatientSerializer,
        responses={201: PatientSerializer, 400: dict},
    )
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class addNewPatientView(APIView):

    def put(self, request, pk):
        pass