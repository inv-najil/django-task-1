from rest_framework import serializers
from .models import Teacher

"""
Validating the Uniqueness of email and employee id
"""
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
    
    def validate_email(self,value):
        if Teacher.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email alredy exists")
        return value
    
    def validate_empid(self,value):
        if Teacher.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee id alredy exists")
        return value