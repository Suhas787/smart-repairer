from rest_framework import serializers
from django.contrib.auth.models import User
from repair.models import DriverProfile, RepairerProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class DriverRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = '__all__'

class RepairerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairerProfile
        fields = '__all__'
