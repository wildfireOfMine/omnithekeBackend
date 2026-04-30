from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from adminApp.models import Administrator
from adminApp.serializers import AdministratorSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

# Create your views here.

class adminView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            admins = Administrator.objects.all()
            serializer = AdministratorSerializer(admins, many=True)
            return Response(serializer.data)
        else:
            admin = Administrator.objects.get(pk=pk)
            serializer = AdministratorSerializer(admin)
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
