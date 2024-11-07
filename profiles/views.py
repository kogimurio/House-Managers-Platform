from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profileView(request):
    user = request.user
    profile_data = {}

    if hasattr(user, 'employer'):
        profile = get_object_or_404(Employer, user=user)
        profile_data = {
            'user_type': 'Employer',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': profile.bio,
            'tribe': profile.tribe,
            'location': profile.location,
            'rating': profile.rating,
            'image': profile.image.url if profile.image else None,
            'hobbies': profile.hobbies,
            'house_type': profile.house_type,
            'number_rooms': profile.number_rooms,
            'number_people': profile.number_people,
            'number_children': profile.number_children,
            'preferred_contract_duration': profile.preferred_contract_duration,
        }

    elif hasattr(user, 'housemanager'):
        profile = get_object_or_404(HouseManager, user=user)
        profile_data = {
            'user_type': 'HouseManager',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': profile.bio,
            'tribe': profile.tribe,
            'location': profile.location,
            'rating': profile.rating,
            'image': profile.image.url if profile.image else None,
            'hobbies': profile.hobbies,
            'education': profile.education,
            'availability': profile.availability,
            'years_of_experience': profile.years_of_experience,
            'skills': profile.skills,
            'age': profile.age,
            'certifications': profile.certifications,
            'languages_spoken': profile.languages_spoken,
            'expected_salary': profile.expected_salary,
            'marital_status': profile.marital_status,
            'income': profile.income,
            'occupation': profile.occupation,
            'gender': profile.gender,
        }
    return JsonResponse(profile_data)
    
    



