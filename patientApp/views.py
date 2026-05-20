from django.shortcuts import render
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from adminApp.serializers import PatientSerializer, DoctorSerializer
from doctorApp.serializers import IncidentSerializer, ReportSerializer, VaccineSerializer, AppointmentSerializer
from patientApp.serializers import MessageSerializer
from doctorApp.models import Doctor, Report, Vaccine
from patientApp.models import Incident, Appointment, Message
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
        summary="PUT your Patient Profile",
        description="Put your own patient profile",
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
    @extend_schema(
        summary="GET your Doctors from your Patient",
        description="Get your doctors from your patient profile",
        responses=DoctorSerializer
    )
    def get(self, request):
        patient = request.user.patient
        doctors = Doctor.objects.filter(patients=patient)
        print(doctors)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

class myIncidentsView(APIView):

    @extend_schema(
        summary="GET your Incidents from your Patient",
        description="Get your incidents from your patient profile",
        responses=IncidentSerializer
    )
    def get(self, request):
        patient = request.user.patient
        incidents = Incident.objects.filter(patient=patient)
        serializer = IncidentSerializer(incidents, many=True)
        return Response(serializer.data)


class myReportsView(APIView):

    @extend_schema(
        summary="GET your Reports from your Patient",
        description="Get your reports from your patient profile",
        responses=ReportSerializer
    )
    def get(self, request):
        patient = request.user.patient
        reports = Report.objects.filter(patient=patient)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

class messagesView(APIView):

    @extend_schema(
        summary="GET your Messages from your Patient",
        description="Get your messages from your patient profile",
        responses=MessageSerializer
    )
    def get(self, request):
        patient = request.user.patient
        messages = Message.objects.filter(patient=patient)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="POST a new Message",
        description="Post a new message in the database",
        request=MessageSerializer,
        responses={201: MessageSerializer, 400: dict},
    )
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class vaccinesView(APIView):

    @extend_schema(
        summary="GET your Vaccines from your Patient",
        description="Get your vaccines from your patient profile",
        responses=VaccineSerializer
    )
    def get(self, request):
        patient = request.user.patient
        vaccines = Vaccine.objects.filter(patient=patient)
        serializer = VaccineSerializer(vaccines, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="POST a new Message",
        description="Post a new message in the database",
        request=VaccineSerializer,
        responses={201: VaccineSerializer, 400: dict},
    )
    def post(self, request):
        serializer = VaccineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class appointmentsView(APIView):

    @extend_schema(
        summary="GET your Appointments from your Patient",
        description="Get your appointments from your patient profile",
        responses=AppointmentSerializer
    )
    def get(self, request):
        patient = request.user.patient
        appointments = Appointment.objects.filter(patient=patient)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="POST a new Message",
        description="Post a new message in the database",
        request=AppointmentSerializer,
        responses={201: AppointmentSerializer, 400: dict},
    )
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)