from rest_framework import serializers
from.models import *
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    username = serializers.CharField(max_length=20)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value
    
    def create(self, validated_data):

        validated_data.pop('password2')

        user = CustomUser.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            password = validated_data['password'],
        )
        return user
            
class LoginSerializer(serializers.Serializer): 
    email = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')   

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("User doesn't exist")  

            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is not active")
            else:
                raise serializers.ValidationError("Incorrect Password")
        else:
            raise serializers.ValidationError("Incorrect Credentials")
        data['user'] = user
        return data

    

    