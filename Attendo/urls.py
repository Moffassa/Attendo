
from django.contrib import admin
from django.urls import path
from Attendo_API import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.UserAPIView.register),
    path('login/', views.UserAPIView.logIn),
    path('resetpassword/', views.UserAPIView.resetPassword),
    path('auth/', views.UserAPIView.auth),
    path('logout/', views.UserAPIView.logOut),
    path('getstudent/',views.StudentView.getStudent),
    path('getinstructor/',views.InstructorView.getInstructor),
    path('getadmin/',views.AdminView.getAdmin),
    path('postlecture/',views.LectureView.postLecture),
    path('putlecture/',views.LectureView.putLecture),
    path('getlectures/',views.LectureView.getInstructorLectures),
    path('getlectures/',views.LectureView.getStudentLectures),
    path('adjustlecturetime/',views.LectureView.adjustLectureTime),
    path('skiplecture/',views.LectureView.skipLecture),
    path('getreport/',views.ReportView.getReport),
    path('startreport/',views.ReportView.startReport),
    path('appendstudent/',views.ReportView.appendStudent)
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
