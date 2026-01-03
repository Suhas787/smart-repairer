from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from repair.models import DriverProfile, RepairerProfile
from .serializers import UserSerializer, DriverRegisterSerializer, RepairerRegisterSerializer
from django.contrib.auth import authenticate

class DriverRegisterAPI(APIView):
    def post(self, request):
        user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
        DriverProfile.objects.create(user=user, vehicle_number=request.data['vehicle_number'],
                                     phone=request.data['phone'], location=request.data['location'])
        return Response({'message': 'Driver registered successfully'})

class RepairerRegisterAPI(APIView):
    def post(self, request):
        user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
        RepairerProfile.objects.create(user=user, workshop_name=request.data['workshop_name'],
                                       service_type=request.data['service_type'],
                                       phone=request.data['phone'], location=request.data['location'])
        return Response({'message': 'Repairer registered successfully'})

class LoginAPI(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            return Response({'message': 'Login successful'})
        return Response({'error': 'Invalid credentials'}, status=400)
