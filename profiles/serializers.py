from rest_framework import serializers
from .models import *
from accounts.models import CustomUser

user = CustomUser

class EmployerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['house_type', 'number_rooms', 'number_people', 'number_children', 'preferred_contract_duration', 'bio', 'location', 'image', 'hobbies', 'tribe' ]

class HouseManagerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseManager
        fields = ['education', 'availability', 'years_of_experience', 'skills', 'age', 'certifications', 'languages_spoken', 'expected_salary', 'marital_status', 'income', 'occupation', 'gender', 'bio', 'location', 'image', 'hobbies', 'tribe']