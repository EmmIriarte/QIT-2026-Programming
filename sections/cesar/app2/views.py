from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Sum, Avg, Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Program, Course, Enrollment, Assignment, Grade


def home(request):
    """
    Home page view - redirects to dashboard if logged in, 
    otherwise shows welcome page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    """
    Main dashboard view showing overview of all programs, 
    courses, and upcoming deadlines.
    """
    user = request.user
    
    # Get all programs user is enrolled in
    user_programs = Program.objects.filter(
        courses__enrollments__user=user
    ).distinct()
    
    # Calculate progress for each program
    programs_with_progress = []
    for program in user_programs:
        earned_ects = program.get_total_ects_earned(user)
        progress_percentage = program.get_progress_percentage(user)
        programs_with_progress.append({
            'program': program,
            'earned_ects': earned_ects,
            'total_ects': program.total_ects_required,
            'progress_percentage': progress_percentage
        })
    
    # Get current enrollments (in progress)
    current_enrollments = Enrollment.objects.filter(
        user=user,
        status='in_progress'
    ).select_related('course', 'course__program')
    
    # Get upcoming assignments (next 7 days)
    today = timezone.now()
    week_from_now = today + timedelta(days=7)
    upcoming_assignments = Assignment.objects.filter(
        course__enrollments__user=user,
        is_completed=False,
        due_date__range=[today, week_from_now]
    ).select_related('course', 'course__program').order_by('due_date')[:10]
    
    # Get overdue assignments
    overdue_assignments = Assignment.objects.filter(
        course__enrollments__user=user,
        is_completed=False,
        due_date__lt=today
    ).select_related('course', 'course__program').order_by('due_date')[:5]
    
    # Calculate overall statistics
    total_courses = Enrollment.objects.filter(user=user).count()
    completed_courses = Enrollment.objects.filter(
        user=user, 
        is_passed=True
    ).count()
    
    # Calculate overall GPA
    all_grades = Grade.objects.filter(
        enrollment__user=user
    )
    if all_grades.exists():
        overall_gpa = all_grades.aggregate(Avg('grade'))['grade__avg']
    else:
        overall_gpa = None
    
    context = {
        'programs_with_progress': programs_with_progress,
        'current_enrollments': current_enrollments,
        'upcoming_assignments': upcoming_assignments,
        'overdue_assignments': overdue_assignments,
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'overall_gpa': round(overall_gpa, 2) if overall_gpa else None,
    }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def course_list(request):
    """
    Display all courses, with filtering options.
    """
    user = request.user
    
    # Get filter parameters
    program_id = request.GET.get('program')
    status = request.GET.get('status')
    semester_type = request.GET.get('semester_type')
    
    # Base query - all user's enrollments
    enrollments = Enrollment.objects.filter(
        user=user
    ).select_related('course', 'course__program')
    
    # Apply filters
    if program_id:
        enrollments = enrollments.filter(course__program_id=program_id)
    if status:
        enrollments = enrollments.filter(status=status)
    if semester_type:
        enrollments = enrollments.filter(course__semester_type=semester_type)
    
    # Get all programs for filter dropdown
    programs = Program.objects.filter(
        courses__enrollments__user=user
    ).distinct()
    
    context = {
        'enrollments': enrollments,
        'programs': programs,
        'selected_program': program_id,
        'selected_status': status,
        'selected_semester_type': semester_type,
    }
    
    return render(request, 'core/course_list.html', context)


@login_required
def course_detail(request, enrollment_id):
    """
    Detailed view of a specific course enrollment.
    Shows assignments, grades, and progress.
    """
    enrollment = get_object_or_404(
        Enrollment.objects.select_related('course', 'course__program'),
        id=enrollment_id,
        user=request.user
    )
    
    # Get all assignments for this course
    assignments = Assignment.objects.filter(
        course=enrollment.course
    ).order_by('due_date')
    
    # Separate into pending and completed
    pending_assignments = assignments.filter(is_completed=False)
    completed_assignments = assignments.filter(is_completed=True)
    
    # Get all grades for this enrollment
    grades = Grade.objects.filter(
        enrollment=enrollment
    ).select_related('assignment').order_by('-date')
    
    # Calculate final grade
    final_grade = enrollment.calculate_final_grade()
    
    # Calculate completion percentage
    completion_percentage = enrollment.get_completion_percentage()
    
    context = {
        'enrollment': enrollment,
        'course': enrollment.course,
        'pending_assignments': pending_assignments,
        'completed_assignments': completed_assignments,
        'grades': grades,
        'final_grade': final_grade,
        'completion_percentage': completion_percentage,
    }
    
    return render(request, 'core/course_detail.html', context)


@login_required
def assignments(request):
    """
    View all assignments across all courses.
    """
    user = request.user
    
    # Get filter parameters
    status = request.GET.get('status', 'pending')  # Default to pending
    program_id = request.GET.get('program')
    
    # Base query
    assignments_query = Assignment.objects.filter(
        course__enrollments__user=user
    ).select_related('course', 'course__program')
    
    # Apply status filter
    if status == 'pending':
        assignments_query = assignments_query.filter(is_completed=False)
    elif status == 'completed':
        assignments_query = assignments_query.filter(is_completed=True)
    elif status == 'overdue':
        assignments_query = assignments_query.filter(
            is_completed=False,
            due_date__lt=timezone.now()
        )
    
    # Apply program filter
    if program_id:
        assignments_query = assignments_query.filter(
            course__program_id=program_id
        )
    
    assignments_list = assignments_query.order_by('due_date')
    
    # Get programs for filter
    programs = Program.objects.filter(
        courses__enrollments__user=user
    ).distinct()
    
    context = {
        'assignments': assignments_list,
        'programs': programs,
        'selected_status': status,
        'selected_program': program_id,
    }
    
    return render(request, 'core/assignments.html', context)


@login_required
def statistics(request):
    """
    Display statistics and charts about academic progress.
    """
    user = request.user
    
    # Get all programs
    programs = Program.objects.filter(
        courses__enrollments__user=user
    ).distinct()
    
    # Calculate GPA per program
    programs_stats = []
    for program in programs:
        enrollments = Enrollment.objects.filter(
            user=user,
            course__program=program
        )
        
        # Get all grades for this program
        grades = Grade.objects.filter(
            enrollment__in=enrollments
        )
        
        if grades.exists():
            avg_grade = grades.aggregate(Avg('grade'))['grade__avg']
        else:
            avg_grade = None
        
        earned_ects = program.get_total_ects_earned(user)
        
        programs_stats.append({
            'program': program,
            'avg_grade': round(avg_grade, 2) if avg_grade else None,
            'earned_ects': earned_ects,
            'remaining_ects': program.total_ects_required - earned_ects,
            'progress_percentage': program.get_progress_percentage(user)
        })
    
    # Overall statistics
    all_grades = Grade.objects.filter(enrollment__user=user)
    overall_gpa = all_grades.aggregate(Avg('grade'))['grade__avg']
    
    # Grade distribution
    grade_distribution = {
        '5.0': all_grades.filter(grade=5.0).count(),
        '4.5': all_grades.filter(grade=4.5).count(),
        '4.0': all_grades.filter(grade=4.0).count(),
        '3.5': all_grades.filter(grade=3.5).count(),
        '3.0': all_grades.filter(grade=3.0).count(),
        '<3.0': all_grades.filter(grade__lt=3.0).count(),
    }
    
    context = {
        'programs_stats': programs_stats,
        'overall_gpa': round(overall_gpa, 2) if overall_gpa else None,
        'grade_distribution': grade_distribution,
    }
    
    return render(request, 'core/statistics.html', context)
