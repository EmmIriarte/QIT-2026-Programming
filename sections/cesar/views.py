from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Sum, Avg
from django.utils import timezone
from django.contrib.auth.models import User

from .schmidt import calculate_schmidt_rank, normalize_state, parse_state_input, get_predefined_states
from .models import Program, Course, Enrollment, Assignment, Grade


def index(request):
    """Main index view for Cesar's section, listing available applications"""
    html = """
    <h1>Cesars Section</h1>
    <ul>
        <li><a href="/cesar/app1/">App 1 - Schmidt Rank</a></li>
        <li><a href="/cesar/app2/">App 2 - Study Planner</a></li>
        <li><a href="/cesar/app3/">App 3 - LeetCode</a></li>
    </ul>
    """
    return HttpResponse(html)


def app1(request):
    """View for the Schmidt Rank Calculator application"""
    
    # Initialize variables to hold calculation results and potential errors
    result = None
    error = None
    
    # Process form submission
    if request.method == 'POST':
        try:
            input_method = request.POST.get('input_method', 'manual')
            
            if input_method == 'manual':
                state_str = request.POST.get('state_vector', '')
                dim_a = int(request.POST.get('dim_a', 2))
                dim_b = int(request.POST.get('dim_b', 2))
                state_vector = parse_state_input(state_str)
                
            elif input_method == 'predefined':
                state_key = request.POST.get('predefined_state')
                states = get_predefined_states()
                state_info = states[state_key]
                state_vector = state_info['vector']
                dim_a, dim_b = state_info['dims']
                
            # Validate dimensions
            if len(state_vector) != dim_a * dim_b:
                raise ValueError(f"State vector size ({len(state_vector)}) doesn't match dimensions {dim_a}×{dim_b}")
            
            state_vector = normalize_state(state_vector)
            
            # Execute main mathematical logic
            result = calculate_schmidt_rank(state_vector, dim_a, dim_b)
            result['state_vector'] = state_vector.tolist()
            result['dim_a'] = dim_a
            result['dim_b'] = dim_b
            
            # Prepare coefficient data for HTML rendering
            max_coeff = max(result['coefficients'])
            coeffs_for_template = []
            for coeff in result['coefficients']:
                coeffs_for_template.append({
                    'value': coeff,
                    'width_percent': (coeff / max_coeff) * 100 if max_coeff > 0 else 0
                })
            result['coefficients'] = coeffs_for_template
            
        except Exception as e:
            error = str(e)
            
    # Gather all data needed by the template into a context dictionary
    context = {
        'result': result,
        'error': error,
        'predefined_states': get_predefined_states()
    }
    
    # Render the HTML template with the context data
    return render(request, "cesar/app1.html", context)

def app2(request):
    """Study Planner - Main Dashboard with actual ORM logic"""
    
    # Grab the first user in the database (your superuser) to act as our student
    user = User.objects.first()
    
    programs_data = []
    current_enrollments = []
    upcoming_assignments = []
    gpa = None
    
    if user:
        # 1. Fetch programs the user is enrolled in
        programs = Program.objects.filter(courses__enrollments__user=user).distinct()
        
        for program in programs:
            # Calculate earned ECTS (sum of ECTS for passed courses in this program)
            earned_result = Enrollment.objects.filter(
                user=user, 
                course__program=program, 
                is_passed=True
            ).aggregate(total_ects=Sum('course__ects'))
            
            earned = earned_result['total_ects'] or 0
            progress = int((earned / program.total_ects_required) * 100) if program.total_ects_required > 0 else 0
            
            programs_data.append({
                'program': program,
                'earned_ects': earned,
                'progress': progress
            })
            
        # 2. Fetch active enrollments
        current_enrollments = Enrollment.objects.filter(user=user, status='in_progress')
        
        # 3. Fetch upcoming assignments (not completed, due date in the future)
        upcoming_assignments = Assignment.objects.filter(
            course__enrollments__user=user,
            is_completed=False,
            due_date__gte=timezone.now()
        ).order_by('due_date')[:5]  # Limit to next 5
        
        # 4. Calculate Overall GPA
        gpa_result = Grade.objects.filter(enrollment__user=user).aggregate(avg_grade=Avg('grade'))
        gpa = gpa_result['avg_grade']

    context = {
        'user_exists': bool(user),
        'programs_data': programs_data,
        'enrollments': current_enrollments,
        'upcoming_assignments': upcoming_assignments,
        'gpa': round(gpa, 2) if gpa else None,
    }
    
    return render(request, "cesar/app2.html", context)

def app3(request):
    """LeetCode Showcase - Reverse Integer (Static display)"""
    
    solution_code = """class Solution:
    def reverse(self, x: int) -> int:
        is_negative = x < 0
        x = abs(x)

        reversed_num = 0
        while x > 0:
            reversed_num = reversed_num * 10 + x % 10
            x //= 10

        if is_negative:
            reversed_num = -reversed_num

        if reversed_num < -2**31 or reversed_num > 2**31 - 1:
            return 0

        return reversed_num"""

    context = {
        'solution_code': solution_code,
    }
    
    return render(request, "cesar/app3.html", context)