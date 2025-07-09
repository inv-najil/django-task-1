from rest_framework import serializers
from .models import Techer

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Techer
        fields = '__all__'
    
    def validate_email(self,value):
        if Techer.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email alredy exists")
        return value
    
    def validate_empid(self,value):
        if Techer.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee id alredy exists")
        return value