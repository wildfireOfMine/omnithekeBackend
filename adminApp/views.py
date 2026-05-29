from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from authApp.serializers import RegisterSerializer
from adminApp.models import Administrator
from doctorApp.models import Doctor
from patientApp.models import Patient
from officeApp.models import Office
from adminApp.serializers import AdministratorSerializer, DoctorSerializer, PatientSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from django.db import transaction

# Create your views here.

class doctorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET all Doctors",
        description="Get a list of all doctors",
        responses=DoctorSerializer(many=True),
    )
    def get(self, request, pk=None):
        office = request.user.administrator.office
        doctors = Doctor.objects.filter(office=office)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="POST a new doctor",
        description="Post a new doctor in the database",
        request=DoctorSerializer,
        responses={201: DoctorSerializer, 400: dict},
    )
    def post(self, request):

        with transaction.atomic():

            userData = {
                "username": request.data.get("name"),
                "email": request.data.get("email"),
                "password": "12345"
            }
            serializerUser = RegisterSerializer(data=userData)
            serializerUser.is_valid(raise_exception=True)
            user = serializerUser.save()
            print(user)

            doctorData = request.data.copy()
            print(doctorData)
            doctorData["djangoUser"] = user.pk
            doctorData["office"] = [request.user.administrator.office.pk]
            serializerDoctor = DoctorSerializer(data=doctorData)
            serializerDoctor.is_valid(raise_exception=True) 

            
            if serializerDoctor.is_valid():
                serializerDoctor.save()
                return Response(serializerDoctor.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializerDoctor.errors, status=status.HTTP_400_BAD_REQUEST)
        

class doctorViewPK(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET a Doctor",
        description="Get a doctor from a PK",
        responses=DoctorSerializer(many=False),
    )
    def get(self, request, pk):
        doctor = Doctor.objects.get(pk=pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)


    @extend_schema(
        summary="PUT a Doctor",
        description="Put a doctor from a PK",
        request=DoctorSerializer,
        responses={201: DoctorSerializer, 400: dict},
    )
    def put(self, request, pk):
        doctor = Doctor.objects.get(pk=pk)
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH a Doctor",
        description="Patch a doctor from a PK",
        request=DoctorSerializer,
        responses={201: DoctorSerializer, 400: dict},
    )
    def patch(self, request, pk):
        doctor = Doctor.objects.get(pk=pk)
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="DELETE a Doctor",
        description="Delete a doctor from a PK",
        responses={204: None},
    )
    def delete(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class patientView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET all Patients",
        description="Get a list of all patients",
        responses=PatientSerializer(many=True),
    )
    def get(self, request, pk=None):
        office = request.user.administrator.office
        patients = Patient.objects.filter(office=office)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="POST a new Patient",
        description="Post a new patient in the database",
        request=PatientSerializer,
        responses={201: PatientSerializer, 400: dict},
    )
    def post(self, request):
        with transaction.atomic():

            userData = {
                "username": request.data.get("name"),
                "email": request.data.get("email"),
                "password": "12345"
            }
            serializerUser = RegisterSerializer(data=userData)
            serializerUser.is_valid(raise_exception=True)
            user = serializerUser.save()
            print(user)

            patientData = request.data.copy()
            print(patientData)
            patientData["djangoUser"] = user.pk
            patientData["office"] = request.user.administrator.office.pk
            patientData["doctors"] = []
            serializerPatient = PatientSerializer(data=patientData)
            serializerPatient.is_valid(raise_exception=True) 

            
            if serializerPatient.is_valid():
                serializerPatient.save()
                return Response(serializerPatient.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializerPatient.errors, status=status.HTTP_400_BAD_REQUEST)

class patientViewPK(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET a Patient",
        description="Get a Patient from a PK",
        responses=PatientSerializer(many=False),
    )
    def get(self, request, pk):
        patient = Patient.objects.get(pk=pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)


    @extend_schema(
        summary="PUT a Patient",
        description="Put a Patient from a PK",
        request=PatientSerializer,
        responses={201: PatientSerializer, 400: dict},
    )
    def put(self, request, pk):
        patient = Patient.objects.get(pk=pk)
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH a Patient",
        description="Patch a Patient from a PK",
        request=PatientSerializer,
        responses={201: PatientSerializer, 400: dict},
    )
    def patch(self, request, pk):
        patient = Patient.objects.get(pk=pk)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="DELETE a Patient",
        description="Delete a Patient from a PK",
        responses={204: None},
    )
    def delete(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class administratorView(APIView):
    @extend_schema(
        summary="GET your Administrator Profile",
        description="Get your administrator profile",
        responses=AdministratorSerializer,
    )
    def get(self, request):
        administrator = request.user.administrator
        serializer = AdministratorSerializer(administrator)
        return Response(serializer.data)
    
    @extend_schema(
        summary="PUT your Administrator Profile",
        description="Put your administrator profile",
        responses=AdministratorSerializer,
    )
    def put(self, request):
        administrator = request.user.administrator
        djangoUser = request.user.administrator.djangoUser.pk
        data = request.data.copy()
        data["djangoUser"] = djangoUser
        data["office"] = request.user.administrator.office.pk
        serializer = AdministratorSerializer(administrator, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)