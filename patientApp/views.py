from django.shortcuts import render
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from adminApp.serializers import PatientSerializer, DoctorSerializer
from doctorApp.models import Doctor
from rest_framework.response import Response
from rest_framework import permissions, status

# Create your views here.

class myProfileView(APIView):

    @extend_schema(
        summary="GET your Patient Profile",
        description="Get your patient profile with all your attributes",
        responses=PatientSerializer,
    )
    def get(self, request):
        patient = request.user.patient
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    
    @extend_schema(
        summary="PUT your Doctor Profile",
        description="Put your own doctor profile",
        request=PatientSerializer,
        responses={201: PatientSerializer, 400: dict},
    )
    def put(self, request):
        patient = request.user.patient
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class myDoctorsView(APIView):
    def get(self, request):
        patient = request.user.patient
        doctors = Doctor.objects.filter(patients=patient)
        print(doctors)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

class myIncidentsView(APIView):
    pass

class messagesView(APIView):
    pass

class vaccinesView(APIView):
    pass

class appointmentsView(APIView):
    pass