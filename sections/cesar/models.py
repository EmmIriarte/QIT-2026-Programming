from django.db import models
from django.contrib.auth.models import User

class Program(models.Model):
    """Represents a study program (e.g. Computer Science)"""
    DEGREE_CHOICES = [
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
    ]
    
    name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    degree_type = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    total_ects_required = models.IntegerField(default=180)
    color = models.CharField(max_length=7, default='#3B82F6')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.university}"

class Course(models.Model):
    """Represents a specific course within a program"""
    SEMESTER_CHOICES = [
        ('fall', 'Fall'),
        ('spring', 'Spring'),
        ('summer', 'Summer'),
    ]
    
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    ects = models.IntegerField(default=6)
    semester_type = models.CharField(max_length=20, choices=SEMESTER_CHOICES, default='fall')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    """Links a User to a Course (Student's progress)"""
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    semester_year = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    is_passed = models.BooleanField(default=False)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.username} - {self.course.code}"

class Assignment(models.Model):
    """Tasks or exams for a specific course"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    weight = models.IntegerField(default=100)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def days_until_due(self):
        from datetime import datetime
        # Zwraca różnicę w dniach
        delta = self.due_date.date() - datetime.now().date()
        return delta.days
    
    def __str__(self):
        return f"{self.title} - {self.course.code}"

class Grade(models.Model):
    """Grades received by a user for assignments or overall course"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grades')
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.DecimalField(max_digits=3, decimal_places=2)
    weight = models.IntegerField(default=100)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.enrollment.user.username} - {self.grade}"