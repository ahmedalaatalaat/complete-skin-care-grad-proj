from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class SkinRecognitionResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SkinRecognitionResult
        fields = '__all__'


class SkinDiseaseResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SkinDiseaseResult
        fields = '__all__'


class SkinBurnDegreeResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SkinBurnDegreeResult
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',  'password']

    
        extra_kwargs = {
            'password': {'write_only':True}
        }


class RegistrationSerializer(serializers.Serializer):
    gender_types = (
        ("M", "Male"),
        ("F", "Female"),
    )
    
    email = serializers.EmailField()
    name = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=20)
    gender = serializers.ChoiceField(gender_types, required=False)
    password = serializers.CharField(min_length=8, max_length=20)
    birthday = serializers.DateField(required=False)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=20)


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.first_name")
    email = serializers.CharField(source="user.username", required=False)
    
    
    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone', 'birthday', 'image', 'gender']


class ResetUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=20, min_length=8)
    new_password = serializers.CharField(max_length=20, min_length=8)

