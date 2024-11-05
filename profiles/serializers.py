from rest_framework import serializers
from .models import *
from accounts.models import CustomUser

user = CustomUser
class EmployerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = Employer
        fields = '__all__'

class HouseManagerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    class Meta:
        model = HouseManager
        fields = '__all__'