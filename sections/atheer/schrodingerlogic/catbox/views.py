from django.shortcuts import render
import random

def catbox_view(request):
    """
    Simulates Schrödinger's cat: alive or dead randomly.
    """
    result = random.choice(["alive", "dead", "superposition"])

    cat_state = f"{result}_cat.png"
    
    context = {"cat_state": cat_state}
    return render(request, "catbox/catbox.html", context)
