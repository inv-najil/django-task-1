from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    
    def validate_email(self,value):
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email alredy exists")
        return value
    
    def validate_roll(self,value):
        if Student.objects.filter(roll_no=value).exists():
            raise serializers.ValidationError("Roll number alredy exists")
        return value