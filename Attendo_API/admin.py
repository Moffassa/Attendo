from django.contrib import admin
from .models import User,Student,Instructor,Admin,Report,Lecture




admin.site.register(User)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Admin)
admin.site.register(Lecture)
admin.site.register(Report)