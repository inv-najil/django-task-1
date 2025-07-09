from django.db import models

class Teacher(models.Model):
    STATUS_CHOICE = (
        ('active','ACTIVE'),
        ('inactive','INACTIVE'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    subject_spl = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=20,unique=True)
    date_of_joining = models.DateField()
    status = models.CharField(max_length=10,choices=STATUS_CHOICE)

    def __str__(self):
        return f"{self.first_name}{self.last_name}"

