from rest_framework import serializers
from django.contrib.auth import authenticate
from django.db import transaction
from .models import User  
from teachers.models import Teacher
from students.models import Student

"""
-login serlizer for authenticating user
"""
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials or user is not active")

"""
Creating a registrion form 
"""
class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    role = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(write_only=True)
    #teacher field
    subject_spl    = serializers.CharField(write_only=True, required=False)
    employee_id    = serializers.CharField(write_only=True, required=False)
    date_of_joining= serializers.DateField(write_only=True, required=False)
    status         = serializers.ChoiceField(choices=Teacher.STATUS_CHOICE, write_only=True, required=False)
    #student fields
    roll_no        = serializers.CharField(write_only=True, required=False)
    grade          = serializers.CharField(write_only=True, required=False)
    dob            = serializers.DateField(write_only=True, required=False)
    admission_date = serializers.DateField(write_only=True, required=False)
    assigned_teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), write_only=True, required=False
    )


    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        if data['role'] not in ['teacher', 'student']:
            raise serializers.ValidationError("Role must be either 'teacher' or 'student'")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        role = validated_data.pop("role")
        phone = validated_data.pop("phone")#poping beacuse phone is common
        
        profile_data = {}
        if role == "teacher":
            for key in ("subject_spl","employee_id","date_of_joining","status"):
                profile_data[key] = validated_data.pop(key)
        else:
            for key in ("roll_no","grade","dob","admission_date","assigined_teacher","status"):
                profile_data[key] = validated_data.pop(key)
        
        with transaction.atomic():#using to solve the issue of partial creation
            user = User(**validated_data, role=role)
            user.set_password(password)
            user.save()

            if role == 'teacher':
                Teacher.objects.create(
                    user=user,
                    first_name = user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    phone=phone,
                    **profile_data
                )
            else:
                Student.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    phone=phone,
                    **profile_data
                )
            return user