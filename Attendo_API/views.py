import datetime
from .models import User,Student,Instructor,Admin,Report,Lecture
from .serializers import UserSerializer,StudentSerializer,InstructorSerializer,AdminSerializer,ReportSerializer,LectureSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
import jwt



def studentAuthCheck():
    try:
       authCheck(type=1)
    except:
       return Response(status=status.HTTP_404_NOT_FOUND)
def instructorAuthCheck():
    try:
       authCheck(type=2)
    except:
       return Response(status=status.HTTP_404_NOT_FOUND)
def adminAuthCheck():
    try:
       authCheck(type=3)
    except:
       return Response(status=status.HTTP_404_NOT_FOUND)
       

def authCheck(request, type):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed("Unauthenticated!")
    
    try:
        payload = jwt.decode(token, 'secret', algorithms="HS256")

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated!")
        
    user = User.objects.filter(id=payload['id'],user_type=payload['user_type']).first()
    if user.user_type != type :
        raise AuthenticationFailed("Unauthenticated!")
        
        



class UserAPIView(APIView):

    @api_view(['POST'])
    def register(request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        return Response(serializer.data)
    
    @api_view(['POST'])
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
            "user_type": user.user_type,
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
    

    
    @api_view(['POST'])
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


    
    @api_view(['POST'])
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

    
    @api_view(['POST'])
    def logOut():
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'successful'
        }

        return response
    



class StudentView(APIView):
    
    @api_view(['POST'])
    def getStudent(request):
        studentAuthCheck
        try:
            id = int(request.data['user_id'])
            student = Student.objects.get(user_id=id)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=StudentSerializer(student)
        return Response(serializer.data)




class InstructorView(APIView):
    
    @api_view(['POST'])
    def getInstructor(request):
        instructorAuthCheck
        try:
            id = int(request.data['user_id'])
            instructor = Instructor.objects.get(user_id=id)
        except Instructor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=InstructorSerializer(instructor)
        return Response(serializer.data)




class AdminView(APIView):

    @api_view(['POST'])
    def getAdmin(request):
        adminAuthCheck
        try:
            id = int(request.data['user_id'])
            admin = Admin.objects.get(user_id=id)
        except Admin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=AdminSerializer(admin)
        return Response(serializer.data)




class LectureView(APIView):


    
    @api_view(['POST'])
    def postLecture(request):
        instructorAuthCheck
        serializer=LectureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


    
    @api_view(['POST'])
    def putLecture(request):
        instructorAuthCheck
        try:
            pk = int(request.data['pk'])
            lecture = Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LectureSerializer(lecture,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    
    @api_view(['POST'])
    def getInstructorLectures(request):
        instructorAuthCheck
        try:
            instructor = request.data['instructor']
            date = datetime.datetime.strptime(request.data['date'], '%Y-%m-%d').date
            min_dt = datetime.datetime.combine(date, datetime.time.min)
            max_dt = datetime.datetime.combine(date, datetime.time.max)
            lectures = Lecture.objects.filter(lecture_start_time__range=(min_dt, max_dt),instructor=instructor)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=LectureSerializer(lectures,many=True)
        return Response(serializer.data)
        

    
    @api_view(['POST'])
    def getStudentLectures(request):
        studentAuthCheck
        try:
            faculty = request.data['faculty']
            grade = request.data['grade']
            date = datetime.datetime.strptime(request.data['date'], '%Y-%m-%d').date
            min_dt = datetime.datetime.combine(date, datetime.time.min)
            max_dt = datetime.datetime.combine(date, datetime.time.max)
            lectures = Lecture.objects.filter(lecture_start_time__range=(min_dt, max_dt),faculty=faculty,grade=grade)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=LectureSerializer(lectures,many=True)
        return Response(serializer.data)
    

    
    @api_view(['POST'])
    def adjustLectureTime(request):
        instructorAuthCheck
        try:
            pk = int(request.data['pk'])
            lecture = Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LectureSerializer(lecture,data=request.data)
        if serializer.is_valid():
            date = datetime.datetime.strptime(request.data['date'], '%Y-%m-%d').date
            start = datetime.datetime.combine(date, datetime.datetime.strptime(request.data['start_time'], "%I:%M %p").time())
            end = datetime.datetime.combine(date, datetime.datetime.strptime(request.data['end_time'], "%I:%M %p").time())
            lecture.lecture_start_time=start
            lecture.lecture_end_time=end
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        

    
    @api_view(['POST'])
    def skipLecture(request):
        instructorAuthCheck
        try:
            pk = int(request.data['pk'])
            lecture = Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        lecture.lecture_start_time += datetime.timedelta(days=7)
        lecture.lecture_end_time += datetime.timedelta(days=7)




class ReportView(APIView):

    
    @api_view(['POST'])
    def getReport(request):
        instructorAuthCheck
        try:
            lecturepk = int(request.data['lecturepk'])
            date = datetime.datetime.strptime(request.data['date'], '%Y-%m-%d').date
            report = Report.objects.get(lecture=lecturepk,date=date)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer=ReportSerializer(report)
        return Response(serializer.data)    
    
    
    @api_view(['POST'])
    def startReport(request):
        instructorAuthCheck
        try:
            lecturepk = int(request.data['lecturepk'])
            report = Report.objects.create(lecture=lecturepk)
            report.date=datetime.date.today()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)     
        report.save()

    
    @api_view(['POST'])
    def appendStudent(request):
        studentAuthCheck
        try:
            lecturepk = int(request.data['lecturepk'])
            student = request.data['student']
            report = Report.objects.get(lecture=lecturepk,date=datetime.date.today())
            report.students.add(student)
            report.authorization_time.append(datetime.now)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)     
        report.save()

