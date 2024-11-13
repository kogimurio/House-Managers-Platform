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
from accounts.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profileView(request):
    user = request.user
    profile_data = {}
    reviews = Review.objects.filter(reviewed=user).values('reviewer__username', 'rating', 'comment', 'created_at')

    if hasattr(user, 'employer'):
        profile = get_object_or_404(Employer, user=user)
        profile_data = {
            'user_type': 'Employer',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'id': user.id,
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
            'reviews': list(reviews)
        }

    elif hasattr(user, 'housemanager'):
        profile = get_object_or_404(HouseManager, user=user)
        profile_data = {
            'user_type': 'HouseManager',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'id': user.id,
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
            'reviews': list(reviews)
        }
    return JsonResponse(profile_data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def create_review(request):
    reviewer = request.user
    reviewed_id = request.data.get('reviewed_id')
    rating = request.data.get('rating')
    comment = request.data.get('comment')

    if reviewer.id == reviewed_id:
        return Response({"message":"You can not review yourself"}, status=status.HTTP_400_BAD_REQUEST)

    reviewed_user = get_object_or_404(CustomUser, id=reviewed_id)
    Review.objects.create(reviewer=reviewer, reviewed=reviewed_user, rating=rating, comment=comment)

    return Response({"message": "Review created successfully"}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated]) 
def employerProfileUpdateView(request):
    try: 
        employer = Employer.objects.get(user=request.user)
        serializer = EmployerProfileUpdateSerializer(employer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your profile has been updated", "Data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Employer.DoesNotExist:
        return Response({"message": "You are not an employer"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def houseManagerProfileUpdateView(request):
    try:
        house_manager = HouseManager.objects.get(user=request.user)
        serializer = HouseManagerProfileUpdateSerializer(house_manager, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your Profile has been updated", "Data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Error updating your profile", "Data": serializer.data}, status=status.HTTP_400_BAD_REQUEST)
    except HouseManager.DoesNotExist:
        return Response({"message": "You are not a house manager"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def searchView(request):
    query = request.GET.get('query', '')
    if query:
        house_manager_results = HouseManager.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )
        employer_results = Employer.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )

        results = {
            "house_managers": [
                {"id": hm.id, "name": hm.name, "description": hm.description, 'location':hm.location} for hm in house_manager_results
            ],
            "employers": [
                {"id": emp.id, "name": emp.name, "description": emp.description, 'location': emp.location} for emp in employer_results
            ],
        }
    else:
        results = {"house_managers": [], "employers": []}
    return JsonResponse(results)

@api_view(['GET'])
def house_manager_detail_view(request, id):
    try:
        house_manager = HouseManager.objects.get(id=id)
        data = {
            "name": house_manager.name,
            "description": house_manager.description,
            "bio": house_manager.bio,
            "tribe": house_manager.tribe,
            "location": house_manager.location,
            "rating": house_manager.rating,
            "image": house_manager.image.url if house_manager.image else None,
            "hobbies": house_manager.hobbies,
            "education": house_manager.education,
            "availability": house_manager.availability,
            "years_of_experience": house_manager.years_of_experience,
            "skills": house_manager.skills,
            "age": house_manager.age,
            "certifications": house_manager.certifications,
            "languages_spoken": house_manager.languages_spoken,
            "expected_salary": house_manager.expected_salary,
            "marital_status": house_manager.marital_status,
            "income": house_manager.income,
            "occupation": house_manager.occupation,
            "gender": house_manager.gender,
            
        }
        return JsonResponse(data)
    except HouseManager.DoesNotExist:
        return Response({"error": "House manager not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def employer_detail_view(request, id):
    try:
        employer = Employer.objects.get(id=id)
        data = {
            "name": employer.name,
            "description": employer.description,
        }
        return JsonResponse(data)
    except Employer.DoesNotExist:
        return Response({"error": "Employer not found"}, status=status.HTTP_404_NOT_FOUND)


