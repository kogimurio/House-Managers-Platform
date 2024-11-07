from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def registerView(request):
    serializers = RegistrationSerializer(data=request.data)

    if serializers.is_valid():
        serializers.save()
        return Response({"success": "You are registered, you can now login"}, status=status.HTTP_200_OK)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def loginView(request):
    serializers = LoginSerializer(data=request.data)

    if serializers.is_valid():
        user = serializers.validated_data['user']
        refresh = RefreshToken.for_user(user)

        refresh['email'] = user.email

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



