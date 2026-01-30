from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
import json
import numpy as np

from .forms import SchmidtCalculatorForm
from .models import Calculation
from .schmidt import (
    calculate_schmidt_decomposition,
    parse_state_input,
    normalize_state,
    get_predefined_states,
    generate_random_state,
    validate_dimensions
)


def home(request):
    """
    Home page with calculator form.
    """
    if request.method == 'POST':
        form = SchmidtCalculatorForm(request.POST)
        if form.is_valid():
            try:
                # Get input method
                input_method = form.cleaned_data['input_method']
                dim_a = form.cleaned_data['dimension_a']
                dim_b = form.cleaned_data['dimension_b']
                state_name = form.cleaned_data.get('state_name', '')
                notes = form.cleaned_data.get('notes', '')
                
                # Get state vector based on input method
                if input_method == 'manual':
                    state_str = form.cleaned_data['state_vector']
                    state_vector = parse_state_input(state_str)
                    
                elif input_method == 'predefined':
                    state_key = form.cleaned_data['predefined_state']
                    predefined_states = get_predefined_states()
                    state_info = predefined_states[state_key]
                    state_vector = state_info['vector']
                    dim_a = state_info['dimensions'][0]
                    dim_b = state_info['dimensions'][1]
                    if not state_name:
                        state_name = state_info['name']
                    
                elif input_method == 'random':
                    random_rank = form.cleaned_data.get('random_rank')
                    state_vector = generate_random_state(dim_a, dim_b, random_rank)
                    if not state_name:
                        state_name = f"Random State ({dim_a}×{dim_b})"
                
                # Validate and normalize
                validate_dimensions(state_vector, dim_a, dim_b)
                state_vector = normalize_state(state_vector)
                
                # Calculate Schmidt decomposition
                result = calculate_schmidt_decomposition(state_vector, dim_a, dim_b)
                
                # Save to database
                calculation = Calculation.objects.create(
                    state_vector=json.dumps(state_vector.tolist()),
                    dimension_a=dim_a,
                    dimension_b=dim_b,
                    state_name=state_name,
                    schmidt_rank=result['schmidt_rank'],
                    schmidt_coefficients=json.dumps(result['schmidt_coefficients']),
                    is_entangled=result['is_entangled'],
                    entropy=result['entropy'],
                    notes=notes
                )
                
                messages.success(request, 'Schmidt rank calculated successfully!')
                return redirect('result', pk=calculation.pk)
                
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = SchmidtCalculatorForm()
    
    # Get recent calculations
    recent_calculations = Calculation.objects.all()[:5]
    
    context = {
        'form': form,
        'recent_calculations': recent_calculations
    }
    return render(request, 'calculator/home.html', context)


def result(request, pk):
    """
    Display calculation results.
    """
    calculation = get_object_or_404(Calculation, pk=pk)
    
    # Parse stored data
    state_vector = calculation.get_state_vector_list()
    coefficients = calculation.get_coefficients_list()
    
    # Prepare data for chart
    chart_data = {
        'labels': [f'λ{i+1}' for i in range(len(coefficients))],
        'values': coefficients
    }
    
    context = {
        'calculation': calculation,
        'state_vector': state_vector,
        'coefficients': coefficients,
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'calculator/result.html', context)


def history(request):
    """
    View all past calculations.
    """
    calculations = Calculation.objects.all()
    
    # Statistics
    total_calculations = calculations.count()
    entangled_count = calculations.filter(is_entangled=True).count()
    product_count = calculations.filter(is_entangled=False).count()
    
    context = {
        'calculations': calculations,
        'total_calculations': total_calculations,
        'entangled_count': entangled_count,
        'product_count': product_count,
    }
    return render(request, 'calculator/history.html', context)


def delete_calculation(request, pk):
    """
    Delete a calculation.
    """
    calculation = get_object_or_404(Calculation, pk=pk)
    calculation.delete()
    messages.success(request, 'Calculation deleted successfully.')
    return redirect('history')


def about(request):
    """
    About page with theory explanation.
    """
    return render(request, 'calculator/about.html')


def api_calculate(request):
    """
    API endpoint for calculation (optional feature).
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        state_vector = np.array(data['state_vector'])
        dim_a = data['dimensions'][0]
        dim_b = data['dimensions'][1]
        
        validate_dimensions(state_vector, dim_a, dim_b)
        state_vector = normalize_state(state_vector)
        
        result = calculate_schmidt_decomposition(state_vector, dim_a, dim_b)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
