from django.http import request
from rest_framework import permissions


class SchoolAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="SchoolAdmin"):
            return True
        
        return False
        


class Student(permissions.BasePermission):


    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="Student"):
            return True

        return False



class Teacher(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="Teacher"):
            return True

        return False


class ParentOrGuardian(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="ParentOrGuardian"):
            return True
        return False







