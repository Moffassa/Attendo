from rest_framework import serializers
from .models import User,Student,Instructor,Admin,Report,Lecture


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields='name','email','phone_number','national_id','user_type'
        read_only_fields=('date_joined','last_updated')
        extra_kwargs = {
            'password': {'write_only': True}}
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields='faculty','grade'
        read_only_fields=('user_id','name')



class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Instructor
        read_only_fields=('user_id','name')



class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model= Admin
        read_only_fields=('user_id','name')
        


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model= Lecture
        fields='instructor','faculty','grade','lecture_start_time','lecture_end_time','students'
        read_only_fields=('pk',)
   
        
        
class ReportSerializer(serializers.ModelSerializer):

    
    class Meta:
      model= Report
      fields='lecture','students','date','authorization_time'