# Main django imports
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import PasswordChangeForm
import jwt 
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
    UserSerializer, ChangePasswordSerializzer, TextBookSerializer
)
from .models import (
    BaseUser, School, TextBook, Subject
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
                    "status" : False,
                    "code" : status.HTTP_307_TEMPORARY_REDIRECT,
                    "message" : "password reset required",
                    "data" : []
                }
                return Response(response, status=status.HTTP_307_TEMPORARY_REDIRECT)
            else:
                org_name = OrganizationUser.objects.get(user__id=baseuser.id).organization.name
                payload = jwt_payload_handler(user)
                print(request.META.get('headers'))
                token = {
                    'token': jwt.encode(payload, SECRET_KEY),
                    'organization': org_name,
                    'status': 'success'
                    }
                print(token)
                return Response(token)
        else:
            return Response(
            {'error': 'Invalid credentials',
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
                    "old_password" : ["Wrong Paswsword"]
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
