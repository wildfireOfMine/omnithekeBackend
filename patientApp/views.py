from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from adminApp.serializers import PatientSerializer, DoctorSerializer
from doctorApp.serializers import IncidentSerializer, ReportSerializer
from patientApp.serializers import MessageSerializer, AppointmentSerializer
from doctorApp.models import Doctor, Report
from patientApp.models import Incident, Appointment, Message, Appointment
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
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
        data = request.data.copy()
        data["djangoUser"] = patient.djangoUser.pk
        data["office"] = patient.office.pk
        data["doctors"] = list(patient.doctors.values_list("pk", flat=True))
        serializer = PatientSerializer(patient, data=data)
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
        active = Incident.objects.filter(patient=patient, active=True)
        old = Incident.objects.filter(patient=patient, active=False)
        return Response({
            "activeIncidents": IncidentSerializer(active, many=True).data,
            "oldIncidents": IncidentSerializer(old, many=True).data
        })


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


class appointmentsView(APIView):

    @extend_schema(
        summary="GET your Appointments from your Patient",
        description="Get your appointments from your patient profile",
        responses=AppointmentSerializer
    )
    def get(self, request):
        patient = request.user.patient
        appointments = Appointment.objects.filter(patient=patient).order_by("-timestamp")
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="POST a new Message",
        description="Post a new message in the database",
        request=AppointmentSerializer,
        responses={201: AppointmentSerializer, 400: dict},
    )
    def post(self, request):
        print(request.data)
        data = request.data.copy()
        data["patient"] = request.user.patient.pk
        data["office"] = request.user.patient.office.pk 
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class appointmentsPKView(APIView):
    def delete(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class availabilityView(APIView):

    def get(self, request, date, pk):
        
        chosenDate = datetime.strptime(date, "%Y-%m-%d").date()
        appointments = Appointment.objects.filter(doctor_id=pk, beginning__date=chosenDate)
        office = request.user.patient.office

        openingHour = office.openingHour.hour
        closingHour = office.closingHour.hour

        occupiedHours = []
        for appointment in appointments:
            localTime = timezone.localtime(appointment.beginning)
            occupiedHours.append(localTime.hour)
        
        availableHours = []
        for hour in range(openingHour, closingHour):
            if hour in occupiedHours:
                print("INSIDE APPOINTMENTS")
            else:
                availableHours.append(f"{hour:02d}:00")
        
        return Response(availableHours)