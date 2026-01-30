from django import forms


class SchmidtCalculatorForm(forms.Form):
    input_method = forms.ChoiceField(choices=[
        ('manual', 'Manual'),
        ('predefined', 'Predefined'),
        ('random', 'Random'),
    ])
    dimension_a = forms.IntegerField(required=False, initial=2)
    dimension_b = forms.IntegerField(required=False, initial=2)
    state_vector = forms.CharField(required=False)
    predefined_state = forms.CharField(required=False)
    state_name = forms.CharField(required=False)
    random_rank = forms.IntegerField(required=False)
    notes = forms.CharField(required=False)
