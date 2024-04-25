import datetime
from .models import User,Student,Instructor,Admin,Report,Lecture
from .serializers import UserSerializer,StudentSerializer,InstructorSerializer,AdminSerializer,ReportSerializer,LectureSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt




class UserAPIView(APIView):
    def register(request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        return Response(serializer.data)
    
    def logIn(request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found:)')
            
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')

       
        payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.now()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        

        response = Response() 

        response.set_cookie(key='jwt', value=token, httponly=True)  

        response.data = {
            'jwt token': token
        }

        return response
    

    def resetPassword(request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms="HS256")

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        serializer.data = request.data
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        return Response(serializer.data)


    def auth(request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms="HS256")

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def logOut():
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'successful'
        }

        return response
    



class StudentView(APIView):
    def getStudent(id):
        try:
            student = Student.objects.get(user_id=id)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=StudentSerializer(student)
        return Response(serializer.data)




class InstructorView(APIView):
    def getInstructor(id):
        try:
            instructor = Instructor.objects.get(user_id=id)
        except Instructor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=InstructorSerializer(instructor)
        return Response(serializer.data)




class AdminView(APIView):
    def getAdmin(id):
        try:
            admin = Admin.objects.get(user_id=id)
        except Admin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=AdminSerializer(admin)
        return Response(serializer.data)




class LectureView(APIView):
    def postLecture(request):
            serializer=LectureSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


    def putLecture(request, pk):
        try:
            lecture = Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LectureSerializer(lecture,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    def getInstructorLectures(instructor, date):
        try:
            min_dt = datetime.datetime.combine(date, datetime.time.min)
            max_dt = datetime.datetime.combine(date, datetime.time.max)
            lectures = Lecture.objects.filter(lecture_start_time__range=(min_dt, max_dt),instructor=instructor)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=LectureSerializer(lectures,many=True)
        return Response(serializer.data)
        
    def getStudentLectures(faculty, grade,date):
        try:
            min_dt = datetime.datetime.combine(date, datetime.time.min)
            max_dt = datetime.datetime.combine(date, datetime.time.max)
            lectures = Lecture.objects.filter(lecture_start_time__range=(min_dt, max_dt),faculty=faculty,grade=grade)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=LectureSerializer(lectures,many=True)
        return Response(serializer.data)
    
    def adjustLectureTime(request, pk, date, start_time, end_time):
        try:
            lecture = Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LectureSerializer(lecture,data=request.data)
        if serializer.is_valid():
            start = datetime.datetime.combine(date, datetime.datetime.strptime(start_time, "%I:%M %p").time())
            end = datetime.datetime.combine(date, datetime.datetime.strptime(end_time, "%I:%M %p").time())
            lecture.lecture_start_time=start
            lecture.lecture_end_time=end
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    def skipLecture(pk):
        try:
            lecture = Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        lecture.lecture_start_time += datetime.timedelta(days=7)
        lecture.lecture_end_time += datetime.timedelta(days=7)




class ReportView(APIView):
    def getReport(lecture, date):
        try:
            report = Report.objects.get(lecture=lecture,date=date)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer=ReportSerializer(report)
        return Response(serializer.data)    
    def startReport(lecture):
        try:
            report = Report.objects.create(lecture=lecture)
            report.date=datetime.date.today()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)     
        report.save()

    def appendStudent(lecture, student):
        try:
            report = Report.objects.get(lecture=lecture,date=datetime.date.today())
            report.students.add(student)
            report.authorization_time.append(datetime.now)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)     
        report.save()

