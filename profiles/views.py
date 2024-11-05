from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def employerView(request):
    if request.method == 'GET':
        employer = Employer.objects.all()
        serializer = EmployerSerializer(employer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



