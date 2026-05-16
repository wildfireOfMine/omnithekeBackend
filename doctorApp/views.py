from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from adminApp.serializers import DoctorSerializer, PatientSerializer
from doctorApp.serializers import NewDoctorSerializer, VaccineSerializer, AppointmentSerializer, IncidentSerializer, MessageSerializer
from doctorApp.models import Vaccine
from patientApp.models import Patient, Appointment, Incident, Message
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


class addNewDoctorView(APIView):

    @extend_schema(
        summary="PATCH a Patient's Doctors",
        description="Patch a patient's doctors, whether adding or erasing",
        request=NewDoctorSerializer,
        responses={201: NewDoctorSerializer, 400: dict},
    )
    def patch(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class vaccinesView(APIView):

    @extend_schema(
        summary="GET all Vaccines",
        description="Get all vaccines from the database",
        request=VaccineSerializer,
        responses=VaccineSerializer,
    )
    def get(self, request):
        vaccines = Vaccine.objects.all()
        serializer = VaccineSerializer(vaccines, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="POST a Vaccine",
        description="Post a vaccine into the database",
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
        
class vaccinesPKView(APIView):

    @extend_schema(
        summary="GET a Vaccine",
        description="Get a vaccine from the database",
        request=VaccineSerializer,
        responses=VaccineSerializer,
    )
    def get(self, request, pk):
        vaccine = Vaccine.objects.get(pk=pk)
        serializer = VaccineSerializer(vaccine)
        return Response(serializer.data)
    
    @extend_schema(
        summary="PUT a Vaccine",
        description="Put a vaccine from the database",
        request=VaccineSerializer,
        responses=VaccineSerializer,
    )
    def put(self, request, pk):
        vaccine = Vaccine.objects.get(pk=pk)
        serializer = VaccineSerializer(vaccine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH a Vaccine",
        description="Patch a vaccine from the database",
        request=VaccineSerializer,
        responses=VaccineSerializer,
    )
    def patch(self, request, pk):
        vaccine = Vaccine.objects.get(pk=pk)
        serializer = VaccineSerializer(vaccine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="DELETE a Vaccine",
        description="Delete a vaccine from the database",
        request=VaccineSerializer,
        responses=VaccineSerializer,
    )
    def delete(self, request, pk):
        vaccine = get_object_or_404(vaccine, pk=pk)
        vaccine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class appointmentsView(APIView):

    @extend_schema(
        summary="GET your Appointments",
        description="Get the appointments with your doctor from the database",
        responses=AppointmentSerializer
    )
    def get(self, request):
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="POST an Appointment",
        description="Post an appointment into the database",
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
        
class appointmentsPKView(APIView):
    @extend_schema(
        summary="GET an Appointment",
        description="Get an appointment with your doctor from the database",
        responses=AppointmentSerializer
    )
    def get(self, request, pk):
        appointment = Appointment.objects.filter(pk=pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    
    @extend_schema(
        summary="PUT an Appointment",
        description="Put an appointment with your doctor from the database",
        request=AppointmentSerializer,
        responses={201: AppointmentSerializer, 400: dict},
    )
    def put(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH an Appointment",
        description="PATCH an appointment with your doctor from the database",
        request=AppointmentSerializer,
        responses={201: AppointmentSerializer, 400: dict},
    )
    def patch(self, request, pk):
        appointment = Appointment.objects.get(pk=pk)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="DELETE an Appointment",
        description="Delete an appointment with your doctor from the database",
        request=VaccineSerializer,
        responses=VaccineSerializer,
    )
    def delete(self, request, pk):
        appointment = get_object_or_404(appointment, pk=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class reportsView(APIView):
    pass

class reportsPKView(APIView):
    pass

class incidentsView(APIView):
    @extend_schema(
        summary="GET your Incidents",
        description="Get the incidents with your doctor from the database",
        responses=IncidentSerializer
    )
    def get(self, request):
        incidents = Incident.objects.filter(doctor=request.user.doctor)
        serializer = IncidentSerializer(incidents, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="POST an Incident",
        description="Post an incident into the database",
        request=IncidentSerializer,
        responses={201: IncidentSerializer, 400: dict},
    )
    def post(self, request):
        serializer = IncidentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class incidentsViewPK(APIView):
    @extend_schema(
        summary="GET an Incident",
        description="Get an incident with your doctor from the database",
        responses=AppointmentSerializer
    )
    def get(self, request, pk):
        incident = Incident.objects.filter(pk=pk)
        serializer = IncidentSerializer(incident)
        return Response(serializer.data)
    
    @extend_schema(
        summary="PUT an Incident",
        description="Put an incident with your doctor from the database",
        request=IncidentSerializer,
        responses={201: IncidentSerializer, 400: dict},
    )
    def put(self, request, pk):
        incident = Incident.objects.get(pk=pk)
        serializer = IncidentSerializer(incident, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH an Incident",
        description="PATCH an incident with your doctor from the database",
        request=IncidentSerializer,
        responses={201: IncidentSerializer, 400: dict},
    )
    def patch(self, request, pk):
        incident = Incident.objects.get(pk=pk)
        serializer = IncidentSerializer(incident, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="DELETE an Incident",
        description="Delete an incident with your doctor from the database",
        request=IncidentSerializer,
        responses=IncidentSerializer,
    )
    def delete(self, request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        incident.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class messagesView(APIView):
    
    @extend_schema(
        summary="GET your Messages",
        description="Get the messages with your doctor from the database",
        responses=MessageSerializer
    )
    def get(self, request):
        messages = Message.objects.filter(doctor=request.user.doctor)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class messagesViewPK(APIView):
    @extend_schema(
        summary="GET a Message",
        description="Get a Message with your doctor from the database",
        responses=MessageSerializer
    )
    def get(self, request, pk):
        message = Message.objects.filter(pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)