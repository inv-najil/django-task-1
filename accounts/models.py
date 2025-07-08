from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICE = (
        ('teacher','TEACHER'),
        ('student','STUDENT'),
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICE)

    def __str__(self):
        return f"{self.username} {(self.role)}"

