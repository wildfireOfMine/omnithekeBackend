from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from hospitalApp.models import Hospital, Department
from drf_spectacular.utils import extend_schema
from hospitalApp.serializers import HospitalSerializer, DepartmentSerializer
from adminApp.serializers import AdministratorSerializer
from adminApp.models import Administrator
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.

class hospitalView(APIView):

    @extend_schema(
        summary="GET your Hospital",
        description="Get your hospital from your administrator profile",
        responses=HospitalSerializer,
    )
    def get(self, request):
        administrator = request.self.administrator
        hospital = Hospital.objects.get(administrator=administrator)
        serializer = HospitalSerializer(hospital, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="POST a new Hospital",
        description="Post a new hospital in the database",
        request=HospitalSerializer,
        responses={201: HospitalSerializer, 400: dict},
    )
    def post(self, request):
        data = request.data.copy()
        data["administrator"] = request.user.administrator.id
        serializer = HospitalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class hospitalPKView(APIView):

    @extend_schema(
        summary="GET a Hospital",
        description="Get a hospital from the database",
        responses=HospitalSerializer,
    )
    def get(self, request, pk):
        hospital = Hospital.objects.get(pk=pk)
        serializer = HospitalSerializer(hospital)
        return Response(serializer.data)

    @extend_schema(
        summary="PUT a Hospital",
        description="Put a hospital from your administrator profile",
        request=HospitalSerializer,
        responses=HospitalSerializer,
    )
    def put(self, request, pk):
        hospital = Hospital.objects.get(pk=pk)
        serializer = HospitalSerializer(hospital, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH a Hospital",
        description="Patch a hospital from your administrator profile",
        request=HospitalSerializer,
        responses={201: HospitalSerializer, 400: dict},
    )
    def patch(self, request, pk):
        hospital = Hospital.objects.get(pk=pk)
        serializer = HospitalSerializer(hospital, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="DELETE a Hospital",
        description="Delete a hospital from your administrator profile",
        request=HospitalSerializer,
        responses=HospitalSerializer,
    )
    def delete(self, request, pk):
        hospital = get_object_or_404(Hospital, pk=pk)
        hospital.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class departmentView(APIView):

    @extend_schema(
        summary="GET all Departments",
        description="Get all departments from your administrator profile",
        responses=DepartmentSerializer,
    )
    def get(self, request):
        administrator = request.self.administrator
        hospital = Hospital.objects.get(administrator=administrator)
        print(hospital.objects.departments)

    @extend_schema(
        summary="POST a new Department",
        description="Post a new department in the database",
        request=DepartmentSerializer,
        responses={201: DepartmentSerializer, 400: dict},
    )
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class departmentPKView(APIView):
    @extend_schema(
        summary="GET a Department",
        description="Get a department from the database",
        responses=DepartmentSerializer,
    )
    def get(self, request, pk):
        department = Department.objects.get(pk=pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    @extend_schema(
        summary="PUT a Department",
        description="Put a department from your administrator profile",
        request=DepartmentSerializer,
        responses=DepartmentSerializer,
    )
    def put(self, request, pk):
        department = Department.objects.get(pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH a Department",
        description="Patch a department from your administrator profile",
        request=DepartmentSerializer,
        responses={201: DepartmentSerializer, 400: dict},
    )
    def patch(self, request, pk):
        department = Department.objects.get(pk=pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="DELETE a Department",
        description="Delete a department from your administrator profile",
        request=DepartmentSerializer,
        responses=DepartmentSerializer,
    )
    def delete(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class administratorView(APIView):

    @extend_schema(
        summary="POST a new Department",
        description="Post a new department in the database",
        request=AdministratorSerializer,
        responses={201: AdministratorSerializer, 400: dict},
    )
    
    def post(self, request):
        data = request.data.copy()
        data["djangoUser"] = request.user.id
        data["email"] = request.user.email
        serializer = AdministratorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class administratorPKView(APIView):
    @extend_schema(
        summary="GET an Administrator",
        description="Get an administrator from the database",
        responses=AdministratorSerializer,
    )
    def get(self, request, pk):
        administrator = Administrator.objects.get(pk=pk)
        serializer = AdministratorSerializer(administrator)
        return Response(serializer.data)

    @extend_schema(
        summary="PUT an Administrator",
        description="Put a hospital from your administrator profile",
        request=AdministratorSerializer,
        responses=AdministratorSerializer,
    )
    def put(self, request, pk):
        administrator = Administrator.objects.get(pk=pk)
        serializer = AdministratorSerializer(administrator, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH an Administrator",
        description="Patch an administsrator from your administrator profile",
        request=AdministratorSerializer,
        responses={201: AdministratorSerializer, 400: dict},
    )
    def patch(self, request, pk):
        administrator = Administrator.objects.get(pk=pk)
        serializer = AdministratorSerializer(administrator, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="DELETE an Administrator",
        description="Delete an administrator from your administrator profile",
        request=AdministratorSerializer,
        responses=AdministratorSerializer,
    )
    def delete(self, request, pk):
        administrator = get_object_or_404(Administrator, pk=pk)
        administrator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
