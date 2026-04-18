from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from adminApp.models import Administrator
from adminApp.serializers import AdministratorSerializer

# Create your views here.

class adminView(APIView):
    def get(self, request, pk=None):
        if pk==None:
            admins = Administrator.objects.all()
            adminsSerialized = AdministratorSerializer(admins, many=True)
            return Response(adminsSerialized.data)
        else:
            admin = Administrator.objects.get(pk=pk)
            adminSerialized = AdministratorSerializer(admin, many=False)
            return Response(adminSerialized.data)

    def post(self, request):
        serializer = AdministratorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class myAccount(APIView):
    def get(self, request):
        return