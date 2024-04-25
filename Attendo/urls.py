
from django.contrib import admin
from django.urls import path, register_converter
from Attendo_API import views, converters
from django.conf import settings
from django.conf.urls.static import static

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.UserAPIView.register),
    path('login/', views.UserAPIView.logIn),
    path('resetpassword/', views.UserAPIView.resetPassword),
    path('auth/', views.UserAPIView.auth),
    path('logout/', views.UserAPIView.logOut),
    path('getstudent/<int:id>/',views.StudentView.getStudent),
    path('getinstructor/<int:id>/',views.InstructorView.getInstructor),
    path('getadmin/<int:id>/',views.AdminView.getAdmin),
    path('postlecture/',views.LectureView.postLecture),
    path('putlecture/<int:pk>/',views.LectureView.putLecture),
    path('getlectures/<str:instructor>/<date:date>/',views.LectureView.getInstructorLectures),
    path('getlectures/<str:faculty>/<str:grade>/<date:date>/',views.LectureView.getStudentLectures),
    path('adjustlecturetime/<int:pk>/<date:date>/<str:start_time>/<str:end_time>/',views.LectureView.adjustLectureTime),
    path('skiplecture/<int:pk>/',views.LectureView.skipLecture),
    path('getreport/<int:lecture>/',views.ReportView.getReport),
    path('startreport/<int:lecture>/',views.ReportView.startReport),
    path('appendstudent/<int:lecture>/<str:student>/',views.ReportView.appendStudent)
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
