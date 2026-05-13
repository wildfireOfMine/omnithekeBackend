from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from doctorApp.serializers import AdministratorSerializer, DoctorSerializer, PatientSerializer, NewDoctorSerializer, VaccineSerializer, AppointmentSerializer
from adminApp.models import Administrator
from doctorApp.models import Doctor, Vaccine
from patientApp.models import Patient, Appointment
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
    def get(self, request):
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    def put(self, request):
        pass

    def patch(self, request):
        pass

    def delete(self, request):
        pass

class messagesView(APIView):
    
    def get(self, request):
        pass