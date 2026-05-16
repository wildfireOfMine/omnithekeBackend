from django.shortcuts import render
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from doctorApp.serializers import DoctorSerializer, PatientSerializer, NewDoctorSerializer, VaccineSerializer, AppointmentSerializer, IncidentSerializer, MessageSerializer
from rest_framework.response import Response

# Create your views here.

class myProfile(APIView):

    @extend_schema(
        summary="GET your Pacient Profile",
        description="Get your pacient profile with all your attributes",
        responses=PatientSerializer,
    )
    def get(self, request):
        patient = request.user.patient
        serializer = PatientSerializer(patient)
        return Response(serializer.data)