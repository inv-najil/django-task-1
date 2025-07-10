from django.db import models
from teachers.models import Teacher
from accounts.models import User

class Student(models.Model):
    STATUS_CHOICE = (
        ('active','ACTIVE'),
        ('inactive','INACTIVE')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True) 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    roll_no = models.CharField(max_length=10,unique=True)
    grade = models.CharField(max_length=10)
    dob = models.DateField()
    admission_date = models.DateField()
    status = models.CharField(max_length=15,choices=STATUS_CHOICE)
    assigned_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='students')
    
    def __str__(self):
        return f"{self.first_name}{self.last_name}"


