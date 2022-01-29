from django.contrib import admin
from .models import (
    School, BaseUser, Subject, TextBook, Level, 
    StudentParentRelation
)



class SchoolAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}

admin.site.register(School, SchoolAdmin)
admin.site.register(BaseUser)
admin.site.register(Subject)
admin.site.register(TextBook)
admin.site.register(Level)
admin.site.register(StudentParentRelation)

# Register your models here.
