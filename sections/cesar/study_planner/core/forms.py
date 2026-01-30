from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Program, Course, Enrollment, Assignment, Grade


class EnrollmentForm(forms.ModelForm):
    """
    Form for creating/editing course enrollments
    """
    class Meta:
        model = Enrollment
        fields = ['course', 'status', 'enrolled_date', 'notes']
        widgets = {
            'enrolled_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Enrollment'))


class AssignmentForm(forms.ModelForm):
    """
    Form for creating/editing assignments
    """
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'assignment_type', 'due_date', 
                 'priority', 'max_points', 'is_completed']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Assignment'))


class GradeForm(forms.ModelForm):
    """
    Form for creating/editing grades
    """
    class Meta:
        model = Grade
        fields = ['assignment', 'grade', 'points', 'max_points', 'weight', 'date', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('assignment', css_class='col-md-6'),
                Column('date', css_class='col-md-6'),
            ),
            Row(
                Column('grade', css_class='col-md-4'),
                Column('points', css_class='col-md-4'),
                Column('max_points', css_class='col-md-4'),
            ),
            Field('weight'),
            Field('comment'),
        )
        self.helper.add_input(Submit('submit', 'Save Grade'))


# More forms can be added as needed
