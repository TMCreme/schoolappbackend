# Main django imports
from datetime import datetime
from email import message
from os import stat
from selectors import BaseSelector
from corsheaders import django
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import PasswordChangeForm
import jwt, json 
from organizations.utils import create_organization
from organizations.models import OrganizationUser, Organization

# Rest framework Imports 
from rest_framework import serializers, status, generics
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, mixins, status, viewsets 
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# In-app imports 
from backend.settings import SECRET_KEY
from .serializers import (
    UserSerializer, ChangePasswordSerializzer, TextBookSerializer, LevelSerializer,
    StudentParentRelationSerializer, SubjectSerializer, 
    PTAScheduleSerializer, AdminRemarkForStudentSerializer,
    TeacherRemarkForStudentSerializer
)
from .models import (
    BaseUser, School, TextBook, Subject, Level, StudentParentRelation, 
    PTASchedule, AdminRemarkForStudent, TeacherRemarkForStudent

)
# from custom_permissions import Teacher, Student, ParentOrGuardian, SchoolAdmin
# I am implementing the custom permissions in views because VS Code was giving me issues when I tried 
# importing from my custom_permissions module above. I will look at this later 

class SchoolAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="SchoolAdmin"):
            return True
        
        return False
class Student(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="Student"):
            return True

        return False
class Teacher(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="Teacher"):
            return True

        return False
class ParentOrGuardian(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="ParentOrGuardian"):
            return True
        return False


def index(request):
    return render(request, "home/index.html")

class LoginUserView(APIView):
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        baseuser = BaseUser.objects.get(username=username)
        user = authenticate(username=username, password=password)
        if user:
            if baseuser.change_password:
                response = {
                    "status" : "Inactive", 
                    "data" : 
                        {
                            "code" : status.HTTP_307_TEMPORARY_REDIRECT,
                            "message" : "password reset required",
                        }
                    
                }
                return Response(response)
            else:
                org_name = OrganizationUser.objects.get(user__id=baseuser.id).organization.name
                mygroup = user.groups.all()[0].name
                payload = jwt_payload_handler(user)
                print(mygroup)
                token = {
                    'status': 'success',
                    'token': jwt.encode(payload, SECRET_KEY),
                    'organization': org_name,
                    "group":mygroup
                    }
                # print(token)
                return Response(token)
        else:
            return Response(
            {'message': 'Invalid credentials',
            'status': 'failed'},
            )

@api_view(['POST'])
@permission_classes((IsAuthenticated,SchoolAdmin))
def create_user(request):
    org_details = request.data["organization"]
    print(org_details)
    serialized = UserSerializer(data=request.data["registration"])
    if serialized.is_valid():
        serialized.save()
        new_user = BaseUser.objects.get(username=request.data["registration"]["username"])
        School.objects.get(name=org_details["name"]).add_user(new_user)
        mygroup = Group.objects.get(name=org_details["group"])
        mygroup.user_set.add(new_user)
        token = {
                'message': "User created successfully",
                'status': 'success'
                }
        return Response(token, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializzer
    model = BaseUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargsa):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            #check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({
                    "old_password" : ["Current password is Wrong"]
                }, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            BaseUser.objects.filter(username=self.object.username).update(change_password=False)
            self.object.save()
            response = {
                "status" : "success",
                "code" : status.HTTP_200_OK,
                "message" : "Password updated successfully, Kindly proceed to login",
                "data" : []
            }
            return Response(response)


# Admin will be able to reset the user's password from this view. 
# This is to handle lost or forgotten password since students might not necessrily have emails addresses

class AdminPasswordResetView(APIView):
    permission_classes = (SchoolAdmin,)

    def post(self, request):
        user = BaseUser.objects.get(username=request.data["username"])
        temp_password = request.data["temp_password"] 
        user.set_password(temp_password)
        user.change_password = True
        user.save()
        return Response({
            "status":"success",
            "message": "User pasword updated sucessfully"
        }, status=status.HTTP_200_OK)



# Simple logout view to delete the auth token in the API calls
class LogoutAPIView(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self,request):
		print(request.user.id)
		request.data.pop('auth_token')
		return Response({'status':'success'})

class TextBookView(generics.ListCreateAPIView):
    # permission_classes = (Student,)
    serializer_class = TextBookSerializer 
    model = TextBook
    queryset = TextBook.objects.all()


# This view is for the School Admin. It will be used for assigning a newly created user to a
# class 
class SchoolAdminStudentView(APIView):
    permission_classes = (SchoolAdmin,)

    def post(self, request):
        org_name = request.data["organization"]
        org_users = OrganizationUser.objects.filter(organization__name=org_name).values_list("user__username")
        students = BaseUser.objects.filter(groups__name="Student").values_list("username")
        print( org_users, students)
        # results = [{"username": name} for [name] in set(org_users) & set(students)]
        results = [name for [name] in set(org_users) & set(students)]
        return Response({
            "status": "success",
            "data" : results
        }, status=status.HTTP_200_OK)



# This view is for asigning a student to a newly added parent. Note that a student must exist before the parent

class StudentParentRelationView(APIView):
    permission_classes = (SchoolAdmin,)

    def post(self, request):
        print(request.data["parent"])
        student = BaseUser.objects.get(username=request.data["student"])
        parent = BaseUser.objects.get(username=request.data["parent"])
        
        StudentParentRelation.objects.create(studentone=student, parent=parent)
        return Response({
            "status" :"success",
            "message" : "Student Linked to Parent Successfully",
            "data": []
        }, status=status.HTTP_200_OK)


from django.core import serializers as dj_serializers
# This view will list all the levels or classes or stages or forms in the school. 
# After creating a student, the student is allocated a class
class StudentLinkLevel(APIView):
    permission_classes = (SchoolAdmin,)

    def post(self, request):
        org_name = School.objects.get(name=request.data["organization"])
        queryset = Level.objects.filter(school__name=request.data["organization"])
        levels = [obj.name for obj in queryset]
        return Response({
            "status": "success",
            "message": "Schools classes retrieved successfully",
            "data" : levels
        }, status=status.HTTP_200_OK)

# This view allows for allocating the student a class. 
class StudentLevelUpdate(APIView):
    permission_classes = (SchoolAdmin,)

    def post(self, request):
        org_name = request.data["organization"]
        level_name = request.data["levelname"]
        student_obj = BaseUser.objects.get(username=request.data["studentname"])
        updated_level = Level.objects.get(name=level_name, school__name=org_name) 
        updated_level.students.add(student_obj)
        return Response({
            "status" : "success",
            "message" : "Student added to the class successfully",
            "data" : []
        })



# This view is for the Admin. It will list all users on the school's account. This will enable the admin 
# to edit the user information. 
class AdminUserList(APIView):
    permission_classes = (SchoolAdmin,)

    def post(self, request):
        org_name = request.data["organization"]
        org_users = OrganizationUser.objects.filter(organization__name=org_name)
        userlist = []
        for user in org_users:
            userlist.append({"username":user.user.username, "group":user.user.groups.all()[0].name})
        return Response({
            "status" : "success",
            "message" : "Users retrieved successfully",
            "data" : userlist
        })


# This view is for Teachers. It lists the subjects together with the level/class/stage/form
# for which the loggedin teacher is assigned to teach. 
class TeacherSubjectView(APIView):
    permission_classes = (Teacher,)

    def post(self, request):
        teacher = request.data["teachername"]
        org_name = request.data["organization"]
        subjects = Subject.objects.filter(teacher__username=teacher, school__name=org_name)
        subjectList = [{
            "name":obj.name, 
            "level" : obj.level.name
        } for obj in subjects]
        return Response({
            "status" : "success",
            "message" : "Subject List retrieved successfully",
            "data" : subjectList
        }, status=status.HTTP_200_OK)




# This view is for Parents. It will list the students together with their level/class/stage/form
class ParentStudentView(APIView):
    permission_classes = (ParentOrGuardian,)

    def post(self, request):
        parentname = request.data["parent"]
        related_student = StudentParentRelation.objects.filter(parent__username=parentname)
        print(related_student)
        student_obj = [{
            "student_name":obj.studentone.username, 
            "level": Level.objects.get(students__username=obj.studentone.username).name
        }for obj in related_student]
        return Response({
            "status" : "succcess",
            "message" : "Students retrieved successfully",
            "data" : student_obj
        }, status=status.HTTP_200_OK)




# This view is for the admin to add PTA Events and view already created upcoming PTA Events
class PTAScheduleView(APIView):
    permission_classes = (SchoolAdmin,) 

    def get(self, request):
        today = datetime.today()
        pta_meeting_list = PTASchedule.objects.filter(start_date__gt=today)
        # print(pta_meeting_list)
        serialized = PTAScheduleSerializer(pta_meeting_list, many=True)
        return Response({
            "status" : "success",
            "message" : "PTA Schedule retrieved Successfully",
            "data" : serialized.data
        })

    def post(self, request, format=None):
        serialized_data = PTAScheduleSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({
                "status" : "success",
                "message" : "PTA Meeting Saved Successfully",
                "data": []
            }, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)



# This view is to add Remark for Students by the Admin 
class AdminRemarkForStudentView(APIView):
    permission_classes = (SchoolAdmin,)

    def post(self, request):
        try:
            school =  School.objects.get(name=request.data["organization"])
            created_by = BaseUser.objects.get(username=request.data["adminusername"])
            student = BaseUser.objects.get(username=request.data["studentusername"])
            remark = request.data["studentremark"]
            serialized_data = AdminRemarkForStudentSerializer(data={
                "created_by": created_by,
                "student": student,
                "school": school,
                "remark": remark
            })
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({
                    "status" : "success",
                    "message" : "Remark Added Successfully",
                    "data" : []
                }, status=status.HTTP_200_OK)
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status" : "failed",
                "message" : " An Error was encountered",
                "error" : str(e)
            }, status=status.HTTP_417_EXPECTATION_FAILED)




# This is a teacher's view to get all students in a particular class. 
# The student automatically belongs to the Subjects list under the class
class StudentListForSubjectView(APIView):
    permission_classes = (Teacher,)

    def post(self, request):
        try:
            subject = request.data["subject"]
            level = request.data["level"]
            print(request.data["organization"])
            student_list = Level.objects.get(school__name=request.data["organization"], name=level).students.all()
            
            student_list = [obj.username for obj in student_list]
            return Response({
                "status" : "success",
                "message" : "Students retrieved sucessfully",
                "data" : student_list
            }, status=status.HTTP_200_OK) 

        except Exception as e:
            return Response({
                "status" : "failed",
                "message" : "An error was encountered",
                "error" : str(e)
            }, status=status.HTTP_200_OK)














































def change_password(request):
    form = PasswordChangeForm(request.POST)
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            request.user.change_password = False
            form.save()
            return Response({
                "message":"Password changed successfully. Kindly proceed to login",
                "status":"success"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message":"Form validation failed. Check and try again",
                "status":"Failed"
            }, status=status.HTTP_400_BAD_REQUEST)
            
    return render(request, "home/change_password.html",{"form":form})










# Create your views here.
