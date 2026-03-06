from django.contrib import admin
from .models import Program, Course, Enrollment, Assignment, Grade

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'degree_type', 'total_ects_required')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'program', 'ects', 'semester_type')
    list_filter = ('program', 'semester_type')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'is_passed')
    list_filter = ('status', 'is_passed')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'is_completed')
    list_filter = ('is_completed', 'course')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'grade', 'weight', 'date')