from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    name = models.CharField(max_length=200)
    total_ects_required = models.IntegerField(default=180)

    def get_total_ects_earned(self, user):
        earned = 0
        for course in self.courses.all():
            enrollment = course.enrollments.filter(user=user, is_passed=True).first()
            if enrollment:
                earned += course.ects
        return earned

    def get_progress_percentage(self, user):
        earned = self.get_total_ects_earned(user)
        if self.total_ects_required == 0:
            return 0
        return round((earned / self.total_ects_required) * 100, 1)

    def __str__(self):
        return self.name


class Course(models.Model):
    SEMESTER_CHOICES = [
        ('winter', 'Winter'),
        ('summer', 'Summer'),
    ]
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    ects = models.IntegerField(default=5)
    semester_type = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='winter')

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    is_passed = models.BooleanField(default=False)

    def calculate_final_grade(self):
        grades = self.grades.all()
        if not grades.exists():
            return None
        return round(grades.aggregate(models.Avg('grade'))['grade__avg'], 2)

    def get_completion_percentage(self):
        total = Assignment.objects.filter(course=self.course).count()
        if total == 0:
            return 0
        completed = Assignment.objects.filter(course=self.course, is_completed=True).count()
        return round((completed / total) * 100, 1)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grades')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    grade = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.enrollment} - {self.grade}"
