from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, HTML
from .schmidt import get_predefined_states


class SchmidtCalculatorForm(forms.Form):
    """
    Form for inputting quantum state for Schmidt rank calculation.
    """
    
    INPUT_METHOD_CHOICES = [
        ('manual', 'Manual Input'),
        ('predefined', 'Predefined State'),
        ('random', 'Random State'),
    ]
    
    input_method = forms.ChoiceField(
        choices=INPUT_METHOD_CHOICES,
        initial='manual',
        widget=forms.RadioSelect,
        label='Input Method'
    )
    
    # Manual input fields
    state_vector = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Enter state vector, e.g.: [0.707, 0, 0, 0.707] or 1, 0, 0, 1'
        }),
        label='State Vector',
        help_text='Enter components separated by commas. Supports complex numbers (e.g., 1+2j)'
    )
    
    dimension_a = forms.IntegerField(
        initial=2,
        min_value=2,
        max_value=10,
        label='Dimension of Subsystem A',
        help_text='Dimension of first subsystem (2-10)'
    )
    
    dimension_b = forms.IntegerField(
        initial=2,
        min_value=2,
        max_value=10,
        label='Dimension of Subsystem B',
        help_text='Dimension of second subsystem (2-10)'
    )
    
    # Predefined state field
    predefined_state = forms.ChoiceField(
        required=False,
        label='Predefined State',
        help_text='Select a well-known quantum state'
    )
    
    # Random state fields
    random_rank = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=10,
        label='Target Schmidt Rank (optional)',
        help_text='Leave empty for completely random state'
    )
    
    # Optional fields
    state_name = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Optional: Give your state a name'
        }),
        label='State Name (optional)'
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Optional: Add notes about this calculation'
        }),
        label='Notes (optional)'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate predefined states choices
        predefined_states = get_predefined_states()
        choices = [('', '--- Select State ---')]
        for key, state_info in predefined_states.items():
            choices.append((key, state_info['name']))
        self.fields['predefined_state'].choices = choices
        
        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('input_method'),
            Div(
                Field('state_vector'),
                Field('dimension_a'),
                Field('dimension_b'),
                css_id='manual-input',
                css_class='input-section'
            ),
            Div(
                Field('predefined_state'),
                css_id='predefined-input',
                css_class='input-section',
                style='display: none;'
            ),
            Div(
                Field('dimension_a'),
                Field('dimension_b'),
                Field('random_rank'),
                css_id='random-input',
                css_class='input-section',
                style='display: none;'
            ),
            Field('state_name'),
            Field('notes'),
            Submit('submit', 'Calculate Schmidt Rank', css_class='btn btn-primary btn-lg')
        )
    
    def clean(self):
        cleaned_data = super().clean()
        input_method = cleaned_data.get('input_method')
        
        if input_method == 'manual':
            state_vector = cleaned_data.get('state_vector')
            if not state_vector:
                raise forms.ValidationError("State vector is required for manual input")
        
        elif input_method == 'predefined':
            predefined_state = cleaned_data.get('predefined_state')
            if not predefined_state:
                raise forms.ValidationError("Please select a predefined state")
        
        return cleaned_data
