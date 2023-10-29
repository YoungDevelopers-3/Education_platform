from django.contrib import admin
from .models import Teacher, Pupil


@admin.register(Pupil)
class PupilAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
