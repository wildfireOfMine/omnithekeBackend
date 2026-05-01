from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from adminApp.models import Administrator
from doctorApp.models import Doctor
from patientApp.models import Patient
from hospitalApp.models import Hospital
from adminApp.serializers import AdministratorSerializer, DoctorSerializer, PatientSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

# Create your views here.

class adminView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AdministratorSerializer,
        responses={201: AdministratorSerializer, 400: dict},
    )
    def get(self, request):
        admins = Administrator.objects.all()
        serializer = AdministratorSerializer(admins, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=AdministratorSerializer,
        responses={201: AdministratorSerializer, 400: dict},
    )
    def post(self, request):
        serializer = AdministratorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class doctorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="",
        description="",
        responses=DoctorSerializer(many=True),
    )
    def get(self, request, pk=None):
        if pk is None:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)
        else:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)

    @extend_schema(
        request=DoctorSerializer,
        responses={201: DoctorSerializer, 400: dict},
    )
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class doctorViewPK(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=DoctorSerializer(many=False),
    )
    def get(self, request, pk):
        doctor = Doctor.objects.get(pk=pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)


    @extend_schema(
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
        summary="",
        description="",
        responses=PatientSerializer(many=True),
    )
    def get(self, request, pk=None):
        if pk is None:
            patients = Patient.objects.all()
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data)
        else:
            patient = Patient.objects.get(pk=pk)
            serializer = PatientSerializer(patient)
            return Response(serializer.data)

    @extend_schema(
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

class patientViewPK(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=PatientSerializer(many=False),
    )
    def get(self, request, pk):
        patient = Patient.objects.get(pk=pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)


    @extend_schema(
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
        responses={204: None},
    )
    def delete(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)