from textwrap import indent
from turtle import back
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from organizations.models import Organization, OrganizationUser
import uuid
from django.conf import settings



class School(Organization):
    date_created = models.DateTimeField(auto_now_add=True,db_index=True)
    date_modified = models.DateTimeField(auto_now=True)
    school_id = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4, editable=False)
    # name = models.CharField(max_length=250)
    # slug = 
    logo = models.ImageField()



class BaseUser(User):
    change_password = models.BooleanField(default=True)







@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse(
        'home:api-password-reset:reset-password-request'
    ),reset_password_token.key)

    send_mail(
        "Password Reset for {title}".format(title="School App"),
        email_plaintext_message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )


class Level(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True)
    levelid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, db_index=True)
    students = models.ManyToManyField(BaseUser, related_name="StudentsInTheClass",blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


    def __str__(self):
        return self.name



class Subject(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True)
    subjectid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    teacher = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="SubjectTeacher")
    name = models.CharField(max_length=250)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="SubjectClass")


    def __str__(self):
        return self.name + " for " +self.level








# Text Books to be uploaded by the schools. 

class TextBook(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True)
    textbookid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    book = models.FileField()


    def __str__(self):
        return self.name
    



class StudentParentRelation(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True)
    parent = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name="Parent")
    studentone = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name="Student")
    


    def __str__(self):
        return self.studentone.username + "'s Parent is : " + self.parent.username.upper()  


    def student(self):
        return 


# class 




# Create your models here.
