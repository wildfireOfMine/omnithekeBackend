from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from officeApp.models import Office, Department
from drf_spectacular.utils import extend_schema
from officeApp.serializers import OfficeSerializer, DepartmentSerializer
from adminApp.serializers import AdministratorSerializer
from adminApp.models import Administrator
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.

class officeView(APIView):

    @extend_schema(
        summary="GET your Office",
        description="Get your office from your administrator profile",
        responses=OfficeSerializer,
    )
    def get(self, request):
        office = request.user.administrator.office
        serializer = OfficeSerializer(office)
        return Response(serializer.data)

    @extend_schema(
        summary="POST a new Office",
        description="Post a new office in the database",
        request=OfficeSerializer,
        responses={201: OfficeSerializer, 400: dict},
    )
    def post(self, request):
        serializer = OfficeSerializer(data=request.data)
        if serializer.is_valid():
            office = serializer.save()

            administrator = request.user.administrator
            administrator.office = office
            administrator.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        office = request.user.administrator.office
        data = request.data.copy()
        data["id"] = office.pk
        serializer = OfficeSerializer(office, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class officePKView(APIView):

    @extend_schema(
        summary="GET an Office",
        description="Get a office from the database",
        responses=OfficeSerializer,
    )
    def get(self, request, pk):
        office = Office.objects.get(pk=pk)
        serializer = OfficeSerializer(office)
        return Response(serializer.data)

    @extend_schema(
        summary="PUT an Office",
        description="Put a office from your administrator profile",
        request=OfficeSerializer,
        responses=OfficeSerializer,
    )
    def put(self, request, pk):
        office = Office.objects.get(pk=pk)
        serializer = OfficeSerializer(office, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH an Office",
        description="Patch an office from your administrator profile",
        request=OfficeSerializer,
        responses={201: OfficeSerializer, 400: dict},
    )
    def patch(self, request, pk):
        office = Office.objects.get(pk=pk)
        serializer = OfficeSerializer(office, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="DELETE an Office",
        description="Delete an office from your administrator profile",
        request=OfficeSerializer,
        responses=OfficeSerializer,
    )
    def delete(self, request, pk):
        office = get_object_or_404(Office, pk=pk)
        office.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class departmentView(APIView):

    @extend_schema(
        summary="GET all Departments",
        description="Get all departments from your administrator profile",
        responses=DepartmentSerializer,
    )
    def get(self, request):
        administrator = request.self.administrator
        office = Office.objects.get(administrator=administrator)
        print(office.objects.departments)

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
        description="Put an administrator from the database",
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
        description="Patch an administrator from your administrator profile",
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
