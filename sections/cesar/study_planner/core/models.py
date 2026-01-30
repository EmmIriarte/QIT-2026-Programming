from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Program(models.Model):
    """
    Represents a university program (e.g., Master's in Quantum Information Technology).
    A user can be enrolled in multiple programs simultaneously.
    """
    DEGREE_CHOICES = [
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('phd', "PhD"),
        ('postdoc', "Postdoctoral"),
    ]
    
    name = models.CharField(
        max_length=200,
        help_text="Full name of the program (e.g., Quantum Information Technology)"
    )
    university = models.CharField(
        max_length=200,
        help_text="University name (e.g., University of Gdańsk)"
    )
    faculty = models.CharField(
        max_length=200,
        blank=True,
        help_text="Faculty or department name"
    )
    degree_type = models.CharField(
        max_length=20,
        choices=DEGREE_CHOICES,
        default='master'
    )
    total_ects_required = models.IntegerField(
        default=120,
        help_text="Total ECTS credits required for graduation"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is this program currently active?"
    )
    color = models.CharField(
        max_length=7,
        default='#3B82F6',
        help_text="Color code for visual identification (hex format, e.g., #3B82F6)"
    )
    description = models.TextField(
        blank=True,
        help_text="Additional information about the program"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'
    
    def __str__(self):
        return f"{self.name} ({self.degree_type})"
    
    def get_total_ects_earned(self, user):
        """Calculate total ECTS earned by a user in this program"""
        enrollments = Enrollment.objects.filter(
            course__program=self,
            user=user,
            is_passed=True
        )
        return sum(e.course.ects for e in enrollments)
    
    def get_progress_percentage(self, user):
        """Get completion percentage for this program"""
        earned = self.get_total_ects_earned(user)
        if self.total_ects_required == 0:
            return 0
        return round((earned / self.total_ects_required) * 100, 2)


class Course(models.Model):
    """
    Represents a course/subject within a program.
    Each course belongs to one program and one semester.
    """
    SEMESTER_TYPE_CHOICES = [
        ('winter', 'Winter Semester'),
        ('summer', 'Summer Semester'),
    ]
    
    COURSE_TYPE_CHOICES = [
        ('mandatory', 'Mandatory'),
        ('elective', 'Elective'),
        ('optional', 'Optional'),
    ]
    
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name='courses',
        help_text="Which program does this course belong to?"
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Course code (e.g., QIT-101)"
    )
    name = models.CharField(
        max_length=200,
        help_text="Course name"
    )
    semester = models.CharField(
        max_length=50,
        help_text="Semester (e.g., Winter 2025/2026)"
    )
    year = models.IntegerField(
        default=1,
        help_text="Year of study (1 or 2 for Master's)"
    )
    semester_type = models.CharField(
        max_length=10,
        choices=SEMESTER_TYPE_CHOICES,
        default='winter'
    )
    ects = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        help_text="ECTS credits"
    )
    course_type = models.CharField(
        max_length=20,
        choices=COURSE_TYPE_CHOICES,
        default='mandatory'
    )
    description = models.TextField(
        blank=True,
        help_text="Course description and syllabus"
    )
    instructor = models.CharField(
        max_length=200,
        blank=True,
        help_text="Instructor name(s)"
    )
    hours_per_week = models.IntegerField(
        default=0,
        help_text="Contact hours per week"
    )
    schedule = models.TextField(
        blank=True,
        help_text="Class schedule (e.g., 'Mon 10:00-12:00, Wed 14:00-16:00')"
    )
    syllabus_url = models.URLField(
        blank=True,
        help_text="Link to course syllabus PDF"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['program', 'year', 'semester_type', 'name']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        unique_together = ['program', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_short_name(self):
        """Return abbreviated course name if too long"""
        if len(self.name) > 40:
            return f"{self.name[:37]}..."
        return self.name


class Enrollment(models.Model):
    """
    Represents a student's enrollment in a specific course.
    Links users to courses and tracks completion status.
    """
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        help_text="Student enrolled in the course"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        help_text="Course being taken"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned'
    )
    enrolled_date = models.DateField(
        default=timezone.now,
        help_text="Date of enrollment"
    )
    is_passed = models.BooleanField(
        default=False,
        help_text="Did the student pass this course?"
    )
    notes = models.TextField(
        blank=True,
        help_text="Personal notes about the course"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-enrolled_date']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        unique_together = ['user', 'course']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.code}"
    
    def calculate_final_grade(self):
        """Calculate weighted final grade from all grades in this enrollment"""
        grades = self.grades.all()
        if not grades:
            return None
        
        total_weight = sum(g.weight for g in grades)
        if total_weight == 0:
            return None
        
        weighted_sum = sum(g.grade * g.weight for g in grades)
        return round(weighted_sum / total_weight, 2)
    
    def get_completion_percentage(self):
        """Get percentage of completed assignments"""
        assignments = Assignment.objects.filter(course=self.course)
        total = assignments.count()
        if total == 0:
            return 0
        completed = assignments.filter(is_completed=True).count()
        return round((completed / total) * 100, 2)


class Assignment(models.Model):
    """
    Represents tasks, projects, exams, or any graded work for a course.
    Each assignment has a due date and can be marked as completed.
    """
    ASSIGNMENT_TYPE_CHOICES = [
        ('homework', 'Homework'),
        ('project', 'Project'),
        ('exam', 'Exam'),
        ('quiz', 'Quiz'),
        ('presentation', 'Presentation'),
        ('lab', 'Lab Work'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments',
        help_text="Course this assignment belongs to"
    )
    title = models.CharField(
        max_length=200,
        help_text="Assignment title"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the assignment"
    )
    assignment_type = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_TYPE_CHOICES,
        default='homework'
    )
    due_date = models.DateTimeField(
        help_text="Deadline for submission"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    max_points = models.FloatField(
        default=100.0,
        validators=[MinValueValidator(0)],
        help_text="Maximum points possible"
    )
    is_completed = models.BooleanField(
        default=False,
        help_text="Has this assignment been completed?"
    )
    completed_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When was this assignment completed?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date']
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"
    
    def is_overdue(self):
        """Check if assignment is past due date"""
        if self.is_completed:
            return False
        return timezone.now() > self.due_date
    
    def days_until_due(self):
        """Calculate days until due date"""
        if self.is_completed:
            return None
        delta = self.due_date - timezone.now()
        return delta.days
    
    def mark_completed(self):
        """Mark assignment as completed"""
        self.is_completed = True
        self.completed_date = timezone.now()
        self.save()


class Grade(models.Model):
    """
    Represents a grade for an assignment or final course grade.
    Supports weighted grading for calculating final course grades.
    """
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='grades',
        help_text="Which enrollment does this grade belong to?"
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grades',
        help_text="Related assignment (optional for final grades)"
    )
    grade = models.FloatField(
        validators=[MinValueValidator(2.0), MaxValueValidator(5.0)],
        help_text="Grade on Polish scale (2.0 - 5.0)"
    )
    points = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Points earned"
    )
    max_points = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Maximum points possible"
    )
    weight = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Weight in final grade calculation (0.0 - 1.0)"
    )
    date = models.DateField(
        default=timezone.now,
        help_text="Date grade was received"
    )
    comment = models.TextField(
        blank=True,
        help_text="Additional comments or feedback"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
    
    def __str__(self):
        course_code = self.enrollment.course.code
        if self.assignment:
            return f"{course_code} - {self.assignment.title}: {self.grade}"
        return f"{course_code} - Final: {self.grade}"
    
    def get_percentage(self):
        """Calculate percentage score if points are available"""
        if self.points is not None and self.max_points and self.max_points > 0:
            return round((self.points / self.max_points) * 100, 2)
        return None
    
    def save(self, *args, **kwargs):
        """Auto-calculate grade from points if not provided"""
        if self.points is not None and self.max_points and not self.grade:
            percentage = (self.points / self.max_points) * 100
            # Convert percentage to Polish grading scale (2.0-5.0)
            if percentage >= 90:
                self.grade = 5.0
            elif percentage >= 80:
                self.grade = 4.5
            elif percentage >= 70:
                self.grade = 4.0
            elif percentage >= 60:
                self.grade = 3.5
            elif percentage >= 50:
                self.grade = 3.0
            else:
                self.grade = 2.0
        super().save(*args, **kwargs)
