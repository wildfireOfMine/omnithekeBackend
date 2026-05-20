from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from authApp.serializers import LoginSerializer, RegisterSerializer, TokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from adminApp.serializers import AdministratorSerializer
from adminApp.models import Administrator

# Create your views here.

class registerView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="POST a User",
        description="Register a user in the database",
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
        summary="GET all Users",
        description="Get all users in the database",
        request=RegisterSerializer,
        responses=RegisterSerializer(many=True),
    )
    def get(self, request):
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data)

class userViewPK(APIView):
    @extend_schema(
        summary="GET a User",
        description="Get a user from a PK",
        request=RegisterSerializer,
        responses=RegisterSerializer(many=True),
    )
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = RegisterSerializer(user)
        return Response(serializer.data)
    
class ObtainToken(TokenObtainPairView):

    serializer_class = TokenSerializer

class adminView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="GET all Administrators",
        description="Get a list of all administrators",
        request=AdministratorSerializer,
        responses={201: AdministratorSerializer, 400: dict},
    )
    def get(self, request):
        admins = Administrator.objects.all()
        serializer = AdministratorSerializer(admins, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="POST an Administrator",
        description="Post a new administrator",
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
