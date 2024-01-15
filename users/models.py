from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

from .managers import CustomUserManager

class StudentGroup(models.Model):
    group_name = models.CharField(max_length=50)
    year = models.IntegerField()
    semester = models.IntegerField()


    def __str__(self):
        return f"{self.group_name} {self.year} {self.semester}"
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)
    is_teacher = models.BooleanField(default=False)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
