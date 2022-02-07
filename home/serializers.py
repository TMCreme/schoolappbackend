from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import (
	BaseUser, School, Subject, TextBook, Level, StudentParentRelation,
	PTASchedule,
)



class UserSerializer(serializers.HyperlinkedModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = BaseUser
		fields = '__all__'
		extra_kwargs = {'id': {'read_only': False}}


	def create(self, validated_data):
		user = super(UserSerializer, self).create(validated_data)
		user.set_password(validated_data['password'])
		user.is_active = True
		user.save()
		return user


class ChangePasswordSerializzer(serializers.Serializer):
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)

	class Meta:
		model = BaseUser
		fields = ["old_password", "new_password"]



class TextBookSerializer(serializers.ModelSerializer):

	class Meta:
		model = TextBook
		fields = "__all__"



class SubjectSerializer(serializers.ModelSerializer):

	class Meta: 
		model: Subject
		fields = "__all__"



class StudentParentRelationSerializer(serializers.ModelSerializer):

	class Meta:
		model = StudentParentRelation 
		fields = "__all__"



class LevelSerializer(serializers.ModelSerializer):

	class Meta: 
		model = Level
		fields = "__all__"




class PTAScheduleSerializer(serializers.ModelSerializer):

	class Meta:
		model = PTASchedule
		fields = "__all__"










