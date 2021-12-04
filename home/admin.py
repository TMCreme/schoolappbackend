from django.contrib import admin
from .models import (
    School, BaseUser, Subject, TextBook
)



class SchoolAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}

admin.site.register(School, SchoolAdmin)
admin.site.register(BaseUser)
admin.site.register(Subject)
admin.site.register(TextBook)

# Register your models here.
