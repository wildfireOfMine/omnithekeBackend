from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from hospitalApp.models import Hospital, Department, Floor, Room
from drf_spectacular.utils import extend_schema
from hospitalApp.serializers import HospitalSerializer, DepartmentSerializer, FloorSerializer, RoomSerializer
from adminApp.serializers import AdministratorSerializer
from adminApp.models import Administrator
from rest_framework import permissions, status
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
        serializer = HospitalSerializer(data=request.data)
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
    
class floorView(APIView):
    @extend_schema(
        summary="GET all Floors",
        description="Get all floors from your administrator profile",
        responses=FloorSerializer,
    )
    def get(self, request):
        administrator = request.self.administrator
        hospital = Hospital.objects.get(administrator=administrator)
        print(hospital.objects.floors)

    @extend_schema(
        summary="POST a new Floor",
        description="Post a new floor in the database",
        request=FloorSerializer,
        responses={201: FloorSerializer, 400: dict},
    )
    def post(self, request):
        serializer = FloorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class floorViewPK(APIView):
    @extend_schema(
        summary="GET a Floor",
        description="Get a floor from the database",
        responses=FloorSerializer,
    )
    def get(self, request, pk):
        floor = Floor.objects.get(pk=pk)
        serializer = FloorSerializer(floor)
        return Response(serializer.data)

    @extend_schema(
        summary="PUT a Floor",
        description="Put a floor from your administrator profile",
        request=FloorSerializer,
        responses=FloorSerializer,
    )
    def put(self, request, pk):
        floor = Floor.objects.get(pk=pk)
        serializer = FloorSerializer(floor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH a Floor",
        description="Patch a floor from your administrator profile",
        request=FloorSerializer,
        responses={201: FloorSerializer, 400: dict},
    )
    def patch(self, request, pk):
        floor = Floor.objects.get(pk=pk)
        serializer = FloorSerializer(floor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="DELETE a Floor",
        description="Delete a floor from your administrator profile",
        request=FloorSerializer,
        responses=FloorSerializer,
    )
    def delete(self, request, pk):
        floor = get_object_or_404(Floor, pk=pk)
        floor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class roomView(APIView):
    @extend_schema(
        summary="GET all Rooms",
        description="Get all rooms from your administrator profile",
        responses=RoomSerializer,
    )
    def get(self, request):
        administrator = request.self.administrator
        hospital = Hospital.objects.get(administrator=administrator)
        print(Room.objects.filter(floor__hospital=hospital))

    @extend_schema(
        summary="POST a new Room",
        description="Post a new room in the database",
        request=RoomSerializer,
        responses={201: RoomSerializer, 400: dict},
    )
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class roomViewPK(APIView):
    @extend_schema(
        summary="GET a Room",
        description="Get a room from the database",
        responses=RoomSerializer,
    )
    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    @extend_schema(
        summary="PUT a Room",
        description="Put a room from your administrator profile",
        request=RoomSerializer,
        responses=RoomSerializer,
    )
    def put(self, request, pk):
        room = Room.objects.get(pk=pk)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="PATCH a Room",
        description="Patch a room from your administrator profile",
        request=RoomSerializer,
        responses={201: RoomSerializer, 400: dict},
    )
    def patch(self, request, pk):
        room = Room.objects.get(pk=pk)
        serializer = RoomSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="DELETE a Room",
        description="Delete a room from your administrator profile",
        request=RoomSerializer,
        responses=RoomSerializer,
    )
    def delete(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class administratorView(APIView):
    @extend_schema(
        summary="GET your Administrator Profile",
        description="Get your administrator profile",
        responses=AdministratorSerializer,
    )
    def get(self, request):
        administrator = request.self.administrator
        serializer = AdministratorSerializer(administrator)
        return Response(serializer.data)

    @extend_schema(
        summary="POST a new Department",
        description="Post a new department in the database",
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
