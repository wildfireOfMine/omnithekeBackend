from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from authApp.serializers import LoginSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

# Create your views here.

class registerView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="",
        description="",
        request=RegisterSerializer,
        responses=RegisterSerializer(many=True),
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class userView(APIView):
    @extend_schema(
        summary="Lists all users",
        description="",
        request=RegisterSerializer,
        responses=RegisterSerializer(many=True),
    )
    def get(self, request):
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data)

class userViewPK(APIView):
    @extend_schema(
        summary="List an user",
        description="",
        request=RegisterSerializer,
        responses=RegisterSerializer(many=True),
    )
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = RegisterSerializer(user)
        return Response(serializer.data)