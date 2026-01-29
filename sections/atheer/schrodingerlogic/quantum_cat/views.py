import random
from django.shortcuts import render

def cat_view(request):
    cat_state = "superposition_cat.png"  # default image
    
    if 'observe' in request.GET:
        # Use full filenames including extension!
        cat_state = random.choice(["alive_cat.png", "dead_cat.png"])
    
    return render(request, 'quantum_cat/cat.html', {'cat_state': cat_state})
