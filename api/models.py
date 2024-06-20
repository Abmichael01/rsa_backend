from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
import uuid



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    approved = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class Hostel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.name

class Block(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.hostel.name)} -- {str(self.name)}"

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.block.hostel.name)} -- {str(self.block.name)} -- {str(self.name)}"

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=70)
    matric_no = models.CharField(max_length=11)
    college = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    student_no = models.CharField(max_length=11)
    parent_no = models.CharField(max_length=11)
    resumption_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{str(self.room.block.hostel.name)} -- {str(self.room.block.name)} -- {str(self.room.name)} -- {str(self.name)}"
