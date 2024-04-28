from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
from .managers import UserManager

    

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
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()


    def save(self, force_insert=False, force_update=False, *args, **kwargs):
      if self._state.adding == True:
        if self.email.__contains__('@stu.com'):
           self.user_type=1
           super(User, self).save(force_insert, force_update, *args, **kwargs)
           student = Student.objects.create(user_id=self, name=self)
           student.save()
        elif self.email.__contains__('@prof.com'):
           self.user_type=2
           super(User, self).save(force_insert, force_update, *args, **kwargs)
           instructor = Instructor.objects.create(user_id=self, name=self)
           instructor.save()
        elif self.email.__contains__('@admin.com'):
           self.user_type=3
           super(User, self).save(force_insert, force_update, *args, **kwargs)
           admin = Admin.objects.create(user_id=self, name=self)
           admin.save()
      else:
           super(User, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.name



class Student(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    name = models.OneToOneField(User, to_field='name',related_name='studentname', on_delete=models.CASCADE)
    faculty = models.CharField(max_length=30, null=True, unique=False)
    grade = models.CharField(max_length=30, null=True, unique=False)

    def save(self, force_insert=False, force_update=False):
        lectures = Lecture.objects.all()
        lectures.save()
        super(Student, self).save(force_insert, force_update)

        
    def __str__(self):
        return self.name




class Instructor(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.OneToOneField(User, to_field='name',related_name='instructorname', on_delete=models.CASCADE)

        
    def __str__(self):
        return self.name




class Admin(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.OneToOneField(User, to_field='name',related_name='adminname', on_delete=models.CASCADE)

        
    def __str__(self):
        return str(self.name)




class Lecture(models.Model):
   name=models.CharField(max_length=50, null=False, unique=True)
   instructor = models.ForeignKey(Instructor, to_field='name', on_delete=models.PROTECT)
   faculty = models.CharField(max_length=30, null=True, unique=False)
   grade = models.CharField(max_length=30, null=True, unique=False)
   lecture_start_time = models.DateTimeField(null=False, blank=False)
   lecture_end_time = models.DateTimeField(null=False, blank=False)
   students = models.ManyToManyField(Student)

   def save(self, force_insert=False, force_update=False):
    students = Student.objects.filter(faculty=self.faculty,grade=self.grade)
    self.students = students
    super(Lecture, self).save(force_insert, force_update)   

        
   def __str__(self):
    return self.name




class Report(models.Model):
   lecture = models.ForeignKey(Lecture, on_delete=models.PROTECT)
   students = models.ManyToManyField(Student)
   date = models.DateField(null=False,blank=False)
   authorization_time = ArrayField(models.TimeField(null=False, blank=False))

        
   def __str__(self):
    return self.lecture.name + " " + self.date
