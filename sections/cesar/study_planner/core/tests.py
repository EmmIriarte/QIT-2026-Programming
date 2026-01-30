from django.test import TestCase
from django.contrib.auth.models import User
from .models import Program, Course, Enrollment, Assignment, Grade


class ProgramModelTest(TestCase):
    """
    Tests for Program model
    """
    def setUp(self):
        self.program = Program.objects.create(
            name="Test Program",
            university="Test University",
            degree_type="master",
            total_ects_required=120
        )
    
    def test_program_creation(self):
        """Test that program is created correctly"""
        self.assertEqual(self.program.name, "Test Program")
        self.assertEqual(self.program.total_ects_required, 120)
    
    def test_program_string_representation(self):
        """Test string representation of program"""
        expected = "Test Program (master)"
        self.assertEqual(str(self.program), expected)


class CourseModelTest(TestCase):
    """
    Tests for Course model
    """
    def setUp(self):
        self.program = Program.objects.create(
            name="Test Program",
            university="Test University"
        )
        self.course = Course.objects.create(
            program=self.program,
            code="TEST-101",
            name="Test Course",
            semester="Winter 2025/2026",
            ects=6
        )
    
    def test_course_creation(self):
        """Test that course is created correctly"""
        self.assertEqual(self.course.code, "TEST-101")
        self.assertEqual(self.course.ects, 6)
    
    def test_course_belongs_to_program(self):
        """Test that course is linked to program"""
        self.assertEqual(self.course.program, self.program)


# Add more tests as needed
