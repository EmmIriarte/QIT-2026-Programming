"""
NOTE FOR FERNANDO: The inline JavaScript logic has been migrated to Python.
All computation (longest palindromic substring, quantum gates, Fibonacci)
now runs server-side. Forms submit via POST and the view returns the result.
"""
import math
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def _expand_around_center(s: str, left: int, right: int) -> int:
    """Expand from center while characters match. Returns length."""
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return right - left - 1


def _longest_palindromic_substring(s: str) -> tuple[str, int, int]:
    """Returns (substring, start_idx, length). Expand-around-center algorithm O(n²)."""
    if not s:
        return "", 0, 0
    start, max_len = 0, 1
    for i in range(len(s)):
        len1 = _expand_around_center(s, i, i)
        len2 = _expand_around_center(s, i, i + 1)
        length = max(len1, len2)
        if length > max_len:
            max_len = length
            start = i - (length - 1) // 2
    return s[start : start + max_len], start, max_len


def index(request):
    """Student index page displaying name and three application links."""
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Emmanuel Aram Iriarte Olea - QIT 2026 Programming</title>
            <style>
                .back-button { padding: 8px 15px; background: #666; color: white; text-decoration: none; border-radius: 4px; display: inline-block; margin-bottom: 20px; }
                .back-button:hover { background: #555; }
            </style>
        </head>
        <body>
            <a href="/" class="back-button">← Back to Global Index</a>
            <h1>Emmanuel Aram Iriarte Olea</h1>
            <ul>
                <li><a href="app1/">Application 1: LeetCode Problem (Longest Palindromic Substring)</a></li>
                <li><a href="app2/">Application 2: Basic Quantum Gates Simulator</a></li>
                <li><a href="app3/">Application 3: Dynamic Programming Example</a></li>
            </ul>
        </body>
        </html>
    """)


SQRT2 = math.sqrt(2)


def _quantum_reset(initial: str) -> list[float]:
    """Return initial quantum state [a00, a01, a10, a11]."""
    states = {
        "00": [1.0, 0.0, 0.0, 0.0],
        "01": [0.0, 1.0, 0.0, 0.0],
        "10": [0.0, 0.0, 1.0, 0.0],
        "11": [0.0, 0.0, 0.0, 1.0],
        "plus": [1 / SQRT2, 0.0, 1 / SQRT2, 0.0],
    }
    return states.get(initial, [1.0, 0.0, 0.0, 0.0])[:]


def _quantum_apply_gate(state: list[float], gate: str) -> list[float]:
    """Apply gate to state. Returns new state. Modifies in place for PauliZ."""
    s = state
    h = 1 / SQRT2
    if gate == "CNOT":
        return [s[0], s[1], s[3], s[2]]
    if gate == "Hadamard":
        return [
            h * (s[0] + s[2]),
            h * (s[1] + s[3]),
            h * (s[0] - s[2]),
            h * (s[1] - s[3]),
        ]
    if gate == "PauliX":
        return [s[2], s[3], s[0], s[1]]
    if gate == "PauliY":
        return [-s[3], -s[2], s[1], s[0]]
    if gate == "PauliZ":
        return [s[0], s[1], -s[2], -s[3]]
    return s[:]


def _app1_result_html(input_val: str) -> str:
    """Build result HTML for longest palindromic substring."""
    if not input_val:
        return '<div id="result" class="success" style="margin-top: 20px; padding: 15px; border-radius: 5px;"><strong>Error:</strong> Please enter a non-empty string.</div>'
    longest, start, max_len = _longest_palindromic_substring(input_val)
    visual_chars = [f'<span class="palindrome">{c}</span>' if start <= i < start + max_len else c for i, c in enumerate(input_val)]
    visual_string = "".join(visual_chars)
    return f'''<div id="result" class="success" style="margin-top: 20px; padding: 15px; border-radius: 5px; background: #d4edda; border: 1px solid #c3e6cb; color: #155724;">
        <strong>Result:</strong> "{longest}"<br>
        <strong>Length:</strong> {max_len}<br>
        <strong>Input:</strong> "{input_val}"<br>
        <div class="string-display">{visual_string}</div>
        <strong>Algorithm:</strong> Expand around centers (O(n²) time, O(1) space) — computed in Python
    </div>'''


@csrf_exempt
def app1(request):
    """Application 1: LeetCode Longest Palindromic Substring Problem (Medium).
    Logic runs in Python (server-side) - no inline JS."""
    input_val = "babad"
    if request.method == "POST":
        input_val = (request.POST.get("input_string") or "").strip() or "babad"
    result_html = _app1_result_html(input_val)

    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Longest Palindromic Substring - LeetCode Medium Problem</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }}
                .back-button {{ padding: 8px 15px; background: #666; color: white; text-decoration: none; border-radius: 4px; display: inline-block; margin-bottom: 20px; }}
                .back-button:hover {{ background: #555; }}
                .problem {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .example {{ background: #e8f4f8; padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; }}
                code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}
                input {{ padding: 8px; margin: 5px; width: 300px; }}
                button {{ padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }}
                button:hover {{ background: #45a049; }}
                .palindrome {{ color: #FF6B6B; font-weight: bold; }}
                .string-display {{ font-family: monospace; font-size: 18px; padding: 15px; background: #f9f9f9; border-radius: 5px; margin: 15px 0; letter-spacing: 2px; }}
            </style>
        </head>
        <body>
            <a href="../" class="back-button">← Back to Index</a>
            <h1>LeetCode Problem: Longest Palindromic Substring (Medium)</h1>
            
            <div class="problem">
                <h2>Problem Description</h2>
                <p>Given a string <code>s</code>, return <em>the longest palindromic substring</em> in <code>s</code>.</p>
                <p>A <strong>palindrome</strong> is a string that reads the same backward as forward.</p>
                <p><strong>Example:</strong></p>
                <p>Input: <code>s = "babad"</code><br>
                Output: <code>"bab"</code> or <code>"aba"</code> (both are valid answers)</p>
            </div>
            
            <div class="example">
                <strong>Example 1:</strong><br>
                Input: s = "babad"<br>
                Output: "bab" or "aba"<br>
                Explanation: Both "bab" and "aba" are palindromes of length 3.
            </div>
            
            <div class="example">
                <strong>Example 2:</strong><br>
                Input: s = "cbbd"<br>
                Output: "bb"<br>
                Explanation: The longest palindromic substring is "bb".
            </div>
            
            <div class="example">
                <strong>Example 3:</strong><br>
                Input: s = "racecar"<br>
                Output: "racecar"<br>
                Explanation: The entire string is a palindrome.
            </div>
            
            <div class="problem">
                <h2>Algorithm Explanation: Expand Around Centers</h2>
                <p><strong>Approach:</strong> Instead of checking every possible substring, we use a more efficient "Expand Around Centers" technique.</p>
                
                <h3>Key Insight:</h3>
                <p>Every palindrome has a center. We can expand from each center position to find the longest palindrome.</p>
                
                <h3>Two Types of Centers:</h3>
                <ol>
                    <li><strong>Odd-length palindromes:</strong> Center is at a single character (e.g., "aba" has center at 'b')</li>
                    <li><strong>Even-length palindromes:</strong> Center is between two characters (e.g., "abba" has center between 'b' and 'b')</li>
                </ol>
                
                <h3>Algorithm Steps:</h3>
                <ol>
                    <li>For each position <code>i</code> in the string:</li>
                    <ul>
                        <li>Check for odd-length palindrome: expand from center <code>(i, i)</code></li>
                        <li>Check for even-length palindrome: expand from center <code>(i, i+1)</code></li>
                    </ul>
                    <li>Expand outward while characters match: <code>s[left] === s[right]</code></li>
                    <li>Keep track of the longest palindrome found</li>
                </ol>
                
                <h3>Time Complexity:</h3>
                <p><strong>O(n²)</strong> - For each of n positions, we potentially expand up to n/2 characters in each direction.</p>
                
                <h3>Space Complexity:</h3>
                <p><strong>O(1)</strong> - Only using a few variables, no additional data structures.</p>
                
                <h3>Example Walkthrough (s = "babad"):</h3>
                <ul>
                    <li><code>i=0</code>: 'b' → expand: len=1 (best so far)</li>
                    <li><code>i=1</code>: 'a' → odd: "bab" (len=3), even: "ba" (len=0) → max=3 ✓</li>
                    <li><code>i=2</code>: 'b' → odd: "aba" (len=3), even: "ba" (len=0) → max=3</li>
                    <li><code>i=3</code>: 'a' → odd: "a" (len=1), even: "ad" (len=0)</li>
                    <li><code>i=4</code>: 'd' → odd: "d" (len=1), even: N/A</li>
                </ul>
                <p><strong>Result:</strong> "bab" or "aba" (both length 3)</p>
            </div>
            
            <h2>Try it yourself:</h2>
            <form method="post" action="">
                <label>Input string:</label><br>
                <input type="text" name="input_string" value="{input_val}" placeholder="Enter a string"><br>
                <button type="submit">Solve</button>
            </form>
            
            {result_html}
        </body>
        </html>
    """
    return HttpResponse(html)


def _app2_state_table(state: list[float]) -> str:
    """Build HTML table for quantum state display."""
    states = ["|00⟩", "|01⟩", "|10⟩", "|11⟩"]
    rows = []
    for i in range(4):
        amp = state[i]
        prob = f"{abs(amp * amp):.3f}"
        amp_str = f"{amp:.3f}"
        rows.append(f"<tr><td>{states[i]}</td><td>{amp_str}</td><td>{prob}</td></tr>")
    return "<table border=\"1\" style=\"border-collapse: collapse; width: 100%;\"><tr><th>State</th><th>Amplitude</th><th>Probability</th></tr>" + "".join(rows) + "</table>"


def _app2_hidden_state_inputs(state: list[float]) -> str:
    """Build hidden inputs for form state."""
    return "".join(f'<input type="hidden" name="s{i}" value="{state[i]}">' for i in range(4))


@csrf_exempt
def app2(request):
    """Application 2: Basic Quantum Gates Simulator. Logic runs in Python (server-side)."""
    state = [1.0, 0.0, 0.0, 0.0]
    initial_sel = "00"
    if request.method == "POST":
        action = request.POST.get("action", "")
        if action == "reset":
            initial_sel = request.POST.get("initial_state", "00")
            state = _quantum_reset(initial_sel)
        else:
            try:
                state = [float(request.POST.get(f"s{i}", 0)) for i in range(4)]
            except (ValueError, TypeError):
                state = [1.0, 0.0, 0.0, 0.0]
            if action in ("PauliX", "PauliY", "PauliZ", "Hadamard", "CNOT"):
                state = _quantum_apply_gate(state, action)
    hidden = _app2_hidden_state_inputs(state)
    state_table = _app2_state_table(state)
    sel_00 = ' selected' if initial_sel == '00' else ''
    sel_01 = ' selected' if initial_sel == '01' else ''
    sel_10 = ' selected' if initial_sel == '10' else ''
    sel_11 = ' selected' if initial_sel == '11' else ''
    sel_plus = ' selected' if initial_sel == 'plus' else ''
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Basic Quantum Gates Simulator</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }}
                .back-button {{ padding: 8px 15px; background: #666; color: white; text-decoration: none; border-radius: 4px; display: inline-block; margin-bottom: 20px; }}
                .back-button:hover {{ background: #555; }}
                .gate-info {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .gate-button {{ padding: 10px 15px; margin: 5px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer; }}
                .gate-button:hover {{ background: #1976D2; }}
                .result {{ margin-top: 20px; padding: 15px; background: #e8f5e9; border-radius: 5px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background-color: #4CAF50; color: white; }}
                .matrix {{ font-family: monospace; }}
            </style>
        </head>
        <body>
            <a href="../" class="back-button">← Back to Index</a>
            <h1>Basic Quantum Gates Simulator</h1>
            
            <div class="gate-info">
                <h2>How to Use the Quantum Gates Simulator</h2>
                <ol>
                    <li><strong>Select Initial State:</strong> Choose a starting quantum state from the dropdown (|00⟩, |01⟩, |10⟩, |11⟩, or |+⟩)</li>
                    <li><strong>Click Reset State:</strong> This sets the starting point - initially only your selected state will have amplitude 1.0, others will be 0.0</li>
                    <li><strong>Apply Gates:</strong> Click on any quantum gate button to transform the current state - gates can create superpositions (multiple states with non-zero amplitudes)</li>
                    <li><strong>View Results:</strong> The table below shows all possible two-qubit states. After applying gates, you may see multiple states with non-zero probabilities.</li>
                </ol>
                <p><strong>Key Point:</strong> The table always shows all 4 possible states (|00⟩, |01⟩, |10⟩, |11⟩). Initially, only your selected state has probability 1.0. After applying gates, quantum superpositions can create multiple states with non-zero amplitudes.</p>
                <p><strong>Gates:</strong> Single-qubit gates operate on the first qubit. CNOT operates on both qubits (flips target if control is |1⟩).</p>
            </div>
            
            <div class="gate-info">
                <h2>Quantum Gates</h2>
                <p>This simulator demonstrates basic single-qubit and two-qubit quantum gates. (Computed in Python)</p>
                
                <h3>Single-Qubit Gates (operate on first qubit):</h3>
                <form method="post" style="display:inline;">{hidden}<input type="hidden" name="action" value="PauliX"><button type="submit" class="gate-button">Pauli-X (Bit Flip)</button></form>
                <form method="post" style="display:inline;">{hidden}<input type="hidden" name="action" value="PauliY"><button type="submit" class="gate-button">Pauli-Y</button></form>
                <form method="post" style="display:inline;">{hidden}<input type="hidden" name="action" value="PauliZ"><button type="submit" class="gate-button">Pauli-Z (Phase Flip)</button></form>
                <form method="post" style="display:inline;">{hidden}<input type="hidden" name="action" value="Hadamard"><button type="submit" class="gate-button">Hadamard (H)</button></form>
                
                <h3>Two-Qubit Gates:</h3>
                <form method="post" style="display:inline;">{hidden}<input type="hidden" name="action" value="CNOT"><button type="submit" class="gate-button">CNOT (Controlled-NOT)</button></form>
            </div>
            
            <form method="post">
                <input type="hidden" name="action" value="reset">
                <h3>Initial State:</h3>
                <select name="initial_state">
                    <option value="00"{sel_00}>|00⟩</option>
                    <option value="01"{sel_01}>|01⟩</option>
                    <option value="10"{sel_10}>|10⟩</option>
                    <option value="11"{sel_11}>|11⟩</option>
                    <option value="plus"{sel_plus}>|+⟩ (Hadamard on |0⟩)</option>
                </select>
                <button type="submit" class="gate-button">Reset State</button>
            </form>
            
            <div id="result" class="result">
                <h3>Current State:</h3>
                <div id="stateDisplay">{state_table}</div>
            </div>
        </body>
        </html>
    """
    return HttpResponse(html)


def _fib_naive(n: int) -> int | None:
    """Naive recursive Fibonacci. Returns None if too slow (n > 35)."""
    if n > 35:
        return None
    if n <= 1:
        return n
    return _fib_naive(n - 1) + _fib_naive(n - 2)


def _fib_dp(n: int, memo: dict | None = None) -> int:
    """Fibonacci with memoization (top-down DP)."""
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
        return n
    memo[n] = _fib_dp(n - 1, memo) + _fib_dp(n - 2, memo)
    return memo[n]


def _fib_tabulation(n: int) -> int:
    """Fibonacci with tabulation (bottom-up DP)."""
    if n <= 1:
        return n
    dp = [0, 1]
    for i in range(2, n + 1):
        dp.append(dp[i - 1] + dp[i - 2])
    return dp[n]


@csrf_exempt
def app3(request):
    """Application 3: Dynamic Programming Example (Fibonacci). Logic runs in Python (server-side)."""
    n_val = 10
    result_html = ""
    if request.method == "POST":
        try:
            n_val = int(request.POST.get("fib_n", 10))
            n_val = max(0, min(45, n_val))
        except (ValueError, TypeError):
            n_val = 10
        start_dp = time.perf_counter()
        result_dp = _fib_dp(n_val)
        time_dp = f"{(time.perf_counter() - start_dp) * 1000:.4f}"
        start_tab = time.perf_counter()
        result_tab = _fib_tabulation(n_val)
        time_tab = f"{(time.perf_counter() - start_tab) * 1000:.4f}"
        result_naive = _fib_naive(n_val)
        if result_naive is not None:
            start_naive = time.perf_counter()
            _ = _fib_naive(n_val)
            time_naive = f"{(time.perf_counter() - start_naive) * 1000:.4f}"
            result_naive_str = str(result_naive)
        else:
            time_naive = "N/A"
            result_naive_str = "N/A (n>35, too slow)"
        result_html = f"""
            <p><strong>F({n_val}) = {result_dp}</strong></p>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr><th>Method</th><th>Result</th><th>Time (ms)</th></tr>
                <tr><td>Dynamic Programming (Memoization)</td><td>{result_dp}</td><td>{time_dp}</td></tr>
                <tr><td>Tabulation (Bottom-up)</td><td>{result_tab}</td><td>{time_tab}</td></tr>
                <tr><td>Naive Recursive (n>35 skipped)</td><td>{result_naive_str}</td><td>{time_naive}</td></tr>
            </table>
            <p><small>Note: Naive recursive skipped for n>35. Computed in Python.</small></p>
        """
    else:
        result_dp = _fib_dp(10)
        result_html = f"""
            <p><strong>F(10) = {result_dp}</strong></p>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr><th>Method</th><th>Result</th><th>Time (ms)</th></tr>
                <tr><td>Dynamic Programming (Memoization)</td><td>{result_dp}</td><td>—</td></tr>
                <tr><td>Tabulation (Bottom-up)</td><td>{result_dp}</td><td>—</td></tr>
                <tr><td>Naive Recursive</td><td>{result_dp}</td><td>—</td></tr>
            </table>
            <p><small>Submit to compute timing. Computed in Python.</small></p>
        """
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dynamic Programming Example</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                .back-button {{ padding: 8px 15px; background: #666; color: white; text-decoration: none; border-radius: 4px; display: inline-block; margin-bottom: 20px; }}
                .back-button:hover {{ background: #555; }}
                .info {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .comparison {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }}
                .method {{ padding: 15px; border: 2px solid #ddd; border-radius: 5px; }}
                .recursive {{ border-color: #f44336; }}
                .dp {{ border-color: #4CAF50; }}
                input {{ padding: 8px; margin: 5px; width: 100px; }}
                button {{ padding: 10px 20px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer; }}
                button:hover {{ background: #1976D2; }}
                .result {{ margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 5px; }}
                code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <a href="../" class="back-button">← Back to Index</a>
            <h1>Dynamic Programming Example: Fibonacci Sequence</h1>
            
            <div class="info">
                <h2>What is Dynamic Programming?</h2>
                <p>Dynamic Programming is a method for solving complex problems by breaking them down into simpler subproblems. 
                It stores the results of subproblems to avoid redundant computations.</p>
                <p><strong>Key concepts:</strong> Memoization (top-down) and Tabulation (bottom-up)</p>
            </div>
            
            <div class="comparison">
                <div class="method recursive">
                    <h3>Naive Recursive Approach</h3>
                    <p><strong>Time Complexity:</strong> O(2^n)</p>
                    <p><strong>Space Complexity:</strong> O(n)</p>
                    <p>Recalculates the same values multiple times.</p>
                </div>
                <div class="method dp">
                    <h3>Dynamic Programming (Memoization)</h3>
                    <p><strong>Time Complexity:</strong> O(n)</p>
                    <p><strong>Space Complexity:</strong> O(n)</p>
                    <p>Stores computed values to avoid recalculation.</p>
                </div>
            </div>
            
            <form method="post">
                <h2>Calculate Fibonacci Number:</h2>
                <label>Enter n (0-45 recommended):</label><br>
                <input type="number" name="fib_n" value="{n_val}" min="0" max="45"><br>
                <button type="submit">Calculate</button>
            </form>
            
            <div id="result" class="result">
                <h3>Results:</h3>
                <div id="resultsDisplay">{result_html}</div>
            </div>
            
            <div class="info">
                <h3>Fibonacci Sequence Definition:</h3>
                <p>F(0) = 0, F(1) = 1</p>
                <p>F(n) = F(n-1) + F(n-2) for n > 1</p>
                <p><strong>Example:</strong> 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...</p>
            </div>
        </body>
        </html>
    """
    return HttpResponse(html)
