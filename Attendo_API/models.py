from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

    

class User(AbstractUser):

    USER_TYPE_CHOICES = (
      (1, 'student'),
      (2, 'instructor'),
      (3, 'admin'),
  )
    
    name=models.CharField(max_length=50, null=False,unique=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    national_id = models.CharField(null=False, blank=False, unique=True, max_length=14)
    user_type = models.PositiveSmallIntegerField(null=False, default=1, blank=False, choices=USER_TYPE_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True,editable=False)
    last_updated = models.DateTimeField(auto_now=True,editable=False)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email




class Student(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    name = models.OneToOneField(User, to_field='name',related_name='studentname', on_delete=models.PROTECT)
    faculty = models.CharField(max_length=30, null=True, unique=False)
    grade = models.CharField(max_length=30, null=True, unique=False)




class Instructor(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.OneToOneField(User, to_field='name',related_name='instructorname', on_delete=models.PROTECT)




class Admin(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.OneToOneField(User, to_field='name',related_name='adminname', on_delete=models.PROTECT)




class Lecture(models.Model):
   instructor = models.ForeignKey(Instructor, to_field='name', on_delete=models.PROTECT)
   faculty = models.CharField(max_length=30, null=True, unique=False)
   grade = models.CharField(max_length=30, null=True, unique=False)
   lecture_start_time = models.DateTimeField(null=False, blank=False)
   lecture_end_time = models.DateTimeField(null=False, blank=False)
   students = models.ManyToManyField(Student)




class Report(models.Model):
   lecture = models.ForeignKey(Lecture, on_delete=models.PROTECT)
   students = models.ManyToManyField(Student)
   date = models.DateField(null=False,blank=False)
   authorization_time = ArrayField(models.DateTimeField(null=False, blank=False))
