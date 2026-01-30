from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np

from .schmidt import (
    calculate_schmidt_decomposition,
    parse_state_input,
    normalize_state,
    get_predefined_states,
    generate_random_state,
    validate_dimensions
)


@csrf_exempt
def home(request):
    """Home page with Schmidt calculator form."""
    result_html = ""
    error_html = ""

    if request.method == 'POST':
        try:
            input_method = request.POST.get('input_method', 'manual')
            dim_a = int(request.POST.get('dimension_a', 2))
            dim_b = int(request.POST.get('dimension_b', 2))
            state_name = request.POST.get('state_name', '')

            if input_method == 'manual':
                state_str = request.POST.get('state_vector', '')
                state_vector = parse_state_input(state_str)
            elif input_method == 'predefined':
                state_key = request.POST.get('predefined_state', 'bell_phi_plus')
                predefined_states = get_predefined_states()
                state_info = predefined_states[state_key]
                state_vector = state_info['vector']
                dim_a = state_info['dimensions'][0]
                dim_b = state_info['dimensions'][1]
                if not state_name:
                    state_name = state_info['name']
            elif input_method == 'random':
                random_rank = request.POST.get('random_rank')
                random_rank = int(random_rank) if random_rank else None
                state_vector = generate_random_state(dim_a, dim_b, random_rank)
                if not state_name:
                    state_name = f"Random State ({dim_a}x{dim_b})"
            else:
                raise ValueError("Invalid input method")

            validate_dimensions(state_vector, dim_a, dim_b)
            state_vector = normalize_state(state_vector)
            calc_result = calculate_schmidt_decomposition(state_vector, dim_a, dim_b)

            name_display = state_name or "Custom State"
            entangled_str = "Yes (Entangled)" if calc_result['is_entangled'] else "No (Product State)"
            coeffs_str = ", ".join(f"{c:.6f}" for c in calc_result['schmidt_coefficients'])

            result_html = f"""
            <div style="background:#e8f5e9;border:1px solid #4caf50;border-radius:8px;padding:20px;margin-top:20px;">
                <h3 style="color:#2e7d32;">Result: {name_display}</h3>
                <table style="width:100%;border-collapse:collapse;">
                    <tr><td style="padding:8px;font-weight:bold;">Dimensions:</td><td>{dim_a} x {dim_b}</td></tr>
                    <tr><td style="padding:8px;font-weight:bold;">Schmidt Rank:</td><td><strong>{calc_result['schmidt_rank']}</strong></td></tr>
                    <tr><td style="padding:8px;font-weight:bold;">Entangled:</td><td>{entangled_str}</td></tr>
                    <tr><td style="padding:8px;font-weight:bold;">Von Neumann Entropy:</td><td>{calc_result['entropy']:.6f}</td></tr>
                    <tr><td style="padding:8px;font-weight:bold;">Schmidt Coefficients:</td><td>{coeffs_str}</td></tr>
                </table>
            </div>
            """
        except Exception as e:
            error_html = f"""
            <div style="background:#ffebee;border:1px solid #f44336;border-radius:8px;padding:15px;margin-top:20px;color:#c62828;">
                <strong>Error:</strong> {str(e)}
            </div>
            """

    predefined_options = ""
    for key, info in get_predefined_states().items():
        predefined_options += f'<option value="{key}">{info["name"]}</option>'

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Schmidt Rank Calculator</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }}
            h1 {{ color: #1565c0; }}
            .form-group {{ margin-bottom: 15px; }}
            label {{ display: block; font-weight: bold; margin-bottom: 5px; color: #333; }}
            input, select {{ width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }}
            button {{ background: #1565c0; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }}
            button:hover {{ background: #0d47a1; }}
            .card {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            .nav {{ margin-bottom: 20px; }}
            .nav a {{ margin-right: 15px; color: #1565c0; text-decoration: none; }}
            .nav a:hover {{ text-decoration: underline; }}
            .hidden {{ display: none; }}
        </style>
    </head>
    <body>
        <div class="nav">
            <a href="/cesar/">&larr; Back to Cesar's Section</a> |
            <a href="/cesar/app1/">Calculator</a> |
            <a href="/cesar/app1/about/">About</a>
        </div>

        <div class="card">
            <h1>Schmidt Rank Calculator</h1>
            <p>Calculate the Schmidt decomposition of a bipartite quantum state to determine its entanglement.</p>

            {error_html}
            {result_html}

            <form method="post" style="margin-top:20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="not_required">
                <div class="form-group">
                    <label>Input Method:</label>
                    <select name="input_method" id="input_method" onchange="toggleInputs()">
                        <option value="manual">Manual Entry</option>
                        <option value="predefined">Predefined State</option>
                        <option value="random">Random State</option>
                    </select>
                </div>

                <div id="manual_inputs">
                    <div class="form-group">
                        <label>State Vector (comma-separated values):</label>
                        <input type="text" name="state_vector" placeholder="e.g. 0.707, 0, 0, 0.707">
                    </div>
                </div>

                <div id="predefined_inputs" class="hidden">
                    <div class="form-group">
                        <label>Predefined State:</label>
                        <select name="predefined_state">
                            {predefined_options}
                        </select>
                    </div>
                </div>

                <div id="dimension_inputs">
                    <div class="form-group" style="display:inline-block;width:48%;">
                        <label>Dimension A:</label>
                        <input type="number" name="dimension_a" value="2" min="2">
                    </div>
                    <div class="form-group" style="display:inline-block;width:48%;">
                        <label>Dimension B:</label>
                        <input type="number" name="dimension_b" value="2" min="2">
                    </div>
                </div>

                <div id="random_inputs" class="hidden">
                    <div class="form-group">
                        <label>Schmidt Rank (optional, leave empty for max):</label>
                        <input type="number" name="random_rank" min="1" placeholder="Auto">
                    </div>
                </div>

                <div class="form-group">
                    <label>State Name (optional):</label>
                    <input type="text" name="state_name" placeholder="e.g. My Bell State">
                </div>

                <button type="submit">Calculate Schmidt Decomposition</button>
            </form>
        </div>

        <script>
            function toggleInputs() {{
                var method = document.getElementById('input_method').value;
                document.getElementById('manual_inputs').className = method === 'manual' ? '' : 'hidden';
                document.getElementById('predefined_inputs').className = method === 'predefined' ? '' : 'hidden';
                document.getElementById('random_inputs').className = method === 'random' ? '' : 'hidden';
                document.getElementById('dimension_inputs').className = method === 'predefined' ? 'hidden' : '';
            }}
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)


def result(request, pk):
    """Display calculation results (placeholder - DB not migrated)."""
    html = """
    <!DOCTYPE html>
    <html><head><title>Result</title></head>
    <body><h1>Result</h1><p>Use the calculator on the <a href="/cesar/app1/">home page</a> to see inline results.</p></body>
    </html>
    """
    return HttpResponse(html)


def history(request):
    """View past calculations (placeholder - DB not migrated)."""
    html = """
    <!DOCTYPE html>
    <html><head><title>History</title></head>
    <body><h1>Calculation History</h1><p>History requires database migrations. Use the <a href="/cesar/app1/">calculator</a> for inline results.</p></body>
    </html>
    """
    return HttpResponse(html)


def delete_calculation(request, pk):
    """Delete a calculation (placeholder)."""
    return HttpResponse("Not available without database migrations.")


def about(request):
    """About page with theory explanation."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>About - Schmidt Decomposition</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }
            h1 { color: #1565c0; }
            h2 { color: #1976d2; }
            .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .nav { margin-bottom: 20px; }
            .nav a { margin-right: 15px; color: #1565c0; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <a href="/cesar/">&larr; Back to Cesar's Section</a> |
            <a href="/cesar/app1/">Calculator</a> |
            <a href="/cesar/app1/about/">About</a>
        </div>

        <div class="card">
            <h1>About Schmidt Decomposition</h1>

            <h2>What is the Schmidt Decomposition?</h2>
            <p>The Schmidt decomposition expresses a pure state of a composite quantum system
            as a sum of bi-orthogonal product states. For any bipartite pure state in H_A &otimes; H_B,
            there exist orthonormal bases such that:</p>
            <p style="text-align:center;font-size:18px;">|&psi;> = &Sigma;<sub>i</sub> &lambda;<sub>i</sub> |i<sub>A</sub>> &otimes; |i<sub>B</sub>></p>

            <h2>Schmidt Rank</h2>
            <p>The <strong>Schmidt rank</strong> is the number of non-zero Schmidt coefficients:</p>
            <ul>
                <li><strong>Rank 1</strong>: Product state (not entangled)</li>
                <li><strong>Rank > 1</strong>: Entangled state</li>
            </ul>

            <h2>Von Neumann Entropy</h2>
            <p>S = -&Sigma;<sub>i</sub> &lambda;<sub>i</sub>&sup2; log<sub>2</sub>(&lambda;<sub>i</sub>&sup2;)</p>
            <p>Higher entropy = more entanglement. Maximum when all Schmidt coefficients are equal.</p>

            <h2>Algorithm</h2>
            <ol>
                <li>Reshape state vector into d_A x d_B matrix</li>
                <li>Perform Singular Value Decomposition (SVD)</li>
                <li>Singular values = Schmidt coefficients</li>
                <li>Count non-zero values = Schmidt rank</li>
            </ol>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def api_calculate(request):
    """API endpoint for Schmidt calculation."""
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
