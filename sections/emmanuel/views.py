from django.http import HttpResponse


def index(request):
    """Student index page displaying name and three application links."""
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Emmanuel - QIT 2026 Programming</title>
        </head>
        <body>
            <h1>Emmanuel</h1>
            <ul>
                <li><a href="app1/">Application 1: LeetCode Problem (Two Sum)</a></li>
                <li><a href="app2/">Application 2: Basic Quantum Gates Simulator</a></li>
                <li><a href="app3/">Application 3: Dynamic Programming Example</a></li>
            </ul>
        </body>
        </html>
    """)


def app1(request):
    """Application 1: LeetCode Two Sum Problem."""
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Two Sum - LeetCode Problem</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                .problem { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .example { background: #e8f4f8; padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; }
                code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
                input { padding: 8px; margin: 5px; width: 300px; }
                button { padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
                button:hover { background: #45a049; }
                #result { margin-top: 20px; padding: 15px; border-radius: 5px; display: none; }
                .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
            </style>
        </head>
        <body>
            <h1>LeetCode Problem: Two Sum</h1>
            
            <div class="problem">
                <h2>Problem Description</h2>
                <p>Given an array of integers <code>nums</code> and an integer <code>target</code>, 
                return <em>indices of the two numbers such that they add up to target</em>.</p>
                <p>You may assume that each input would have <strong>exactly one solution</strong>, 
                and you may not use the same element twice.</p>
                <p>You can return the answer in any order.</p>
            </div>
            
            <div class="example">
                <strong>Example 1:</strong><br>
                Input: nums = [2,7,11,15], target = 9<br>
                Output: [0,1]<br>
                Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
            </div>
            
            <div class="example">
                <strong>Example 2:</strong><br>
                Input: nums = [3,2,4], target = 6<br>
                Output: [1,2]
            </div>
            
            <h2>Try it yourself:</h2>
            <div>
                <label>Array (comma-separated integers):</label><br>
                <input type="text" id="nums" value="2,7,11,15" placeholder="2,7,11,15"><br>
                <label>Target:</label><br>
                <input type="number" id="target" value="9" placeholder="9"><br>
                <button onclick="solveTwoSum()">Solve</button>
            </div>
            
            <div id="result"></div>
            
            <script>
                function solveTwoSum() {
                    const numsStr = document.getElementById('nums').value;
                    const target = parseInt(document.getElementById('target').value);
                    
                    // Parse array
                    const nums = numsStr.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
                    
                    // Algorithm: Hash map approach (O(n) time complexity)
                    const map = {};
                    for (let i = 0; i < nums.length; i++) {
                        const complement = target - nums[i];
                        if (map[complement] !== undefined) {
                            document.getElementById('result').innerHTML = 
                                '<strong>Result:</strong> [' + map[complement] + ', ' + i + ']<br>' +
                                '<strong>Explanation:</strong> nums[' + map[complement] + '] + nums[' + i + '] = ' + 
                                nums[map[complement]] + ' + ' + nums[i] + ' = ' + target;
                            document.getElementById('result').style.display = 'block';
                            document.getElementById('result').className = 'success';
                            return;
                        }
                        map[nums[i]] = i;
                    }
                    
                    document.getElementById('result').innerHTML = 
                        '<strong>No solution found!</strong> There is no pair that adds up to ' + target;
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('result').className = 'success';
                }
            </script>
        </body>
        </html>
    """
    return HttpResponse(html)


def app2(request):
    """Application 2: Basic Quantum Gates Simulator."""
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Basic Quantum Gates Simulator</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
                .gate-info { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .gate-button { padding: 10px 15px; margin: 5px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer; }
                .gate-button:hover { background: #1976D2; }
                .result { margin-top: 20px; padding: 15px; background: #e8f5e9; border-radius: 5px; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
                th { background-color: #4CAF50; color: white; }
                .matrix { font-family: monospace; }
            </style>
        </head>
        <body>
            <h1>Basic Quantum Gates Simulator</h1>
            
            <div class="gate-info">
                <h2>Quantum Gates</h2>
                <p>This simulator demonstrates basic single-qubit and two-qubit quantum gates.</p>
                
                <h3>Single-Qubit Gates:</h3>
                <button class="gate-button" onclick="applyGate('PauliX')">Pauli-X (Bit Flip)</button>
                <button class="gate-button" onclick="applyGate('PauliY')">Pauli-Y</button>
                <button class="gate-button" onclick="applyGate('PauliZ')">Pauli-Z (Phase Flip)</button>
                <button class="gate-button" onclick="applyGate('Hadamard')">Hadamard (H)</button>
                
                <h3>Two-Qubit Gates:</h3>
                <button class="gate-button" onclick="applyGate('CNOT')">CNOT (Controlled-NOT)</button>
            </div>
            
            <div>
                <h3>Initial State:</h3>
                <select id="initialState">
                    <option value="00">|00⟩</option>
                    <option value="01">|01⟩</option>
                    <option value="10">|10⟩</option>
                    <option value="11">|11⟩</option>
                    <option value="plus">|+⟩ (Hadamard on |0⟩)</option>
                </select>
                <button class="gate-button" onclick="resetState()">Reset</button>
            </div>
            
            <div id="result" class="result" style="display:none;">
                <h3>Current State:</h3>
                <div id="stateDisplay"></div>
            </div>
            
            <script>
                // Quantum state representation: [amplitude_00, amplitude_01, amplitude_10, amplitude_11]
                let currentState = [1, 0, 0, 0]; // |00⟩
                
                // Gate matrices (in computational basis)
                const gates = {
                    'PauliX': [[0, 1], [1, 0]],  // X gate
                    'PauliY': [[0, -1j], [1j, 0]],  // Y gate (approximation)
                    'PauliZ': [[1, 0], [0, -1]],  // Z gate
                    'Hadamard': [[1/Math.SQRT2, 1/Math.SQRT2], [1/Math.SQRT2, -1/Math.SQRT2]]
                };
                
                function resetState() {
                    const select = document.getElementById('initialState').value;
                    switch(select) {
                        case '00': currentState = [1, 0, 0, 0]; break;
                        case '01': currentState = [0, 1, 0, 0]; break;
                        case '10': currentState = [0, 0, 1, 0]; break;
                        case '11': currentState = [0, 0, 0, 1]; break;
                        case 'plus': currentState = [1/Math.SQRT2, 0, 1/Math.SQRT2, 0]; break;
                    }
                    updateDisplay();
                }
                
                function applyGate(gateName) {
                    if (gateName === 'CNOT') {
                        // CNOT flips target qubit if control is |1⟩
                        // |00⟩ -> |00⟩, |01⟩ -> |01⟩, |10⟩ -> |11⟩, |11⟩ -> |10⟩
                        const newState = [...currentState];
                        currentState[0] = newState[0]; // |00⟩ unchanged
                        currentState[1] = newState[1]; // |01⟩ unchanged
                        currentState[2] = newState[3]; // |10⟩ -> |11⟩
                        currentState[3] = newState[2]; // |11⟩ -> |10⟩
                    } else if (gateName === 'Hadamard') {
                        // Apply Hadamard to first qubit (simplified)
                        const h = 1/Math.SQRT2;
                        const newState = [
                            h * (currentState[0] + currentState[2]),
                            h * (currentState[1] + currentState[3]),
                            h * (currentState[0] - currentState[2]),
                            h * (currentState[1] - currentState[3])
                        ];
                        currentState = newState;
                    } else if (gateName === 'PauliX') {
                        // X gate flips |0⟩ and |1⟩ on first qubit
                        const newState = [currentState[2], currentState[3], currentState[0], currentState[1]];
                        currentState = newState;
                    } else if (gateName === 'PauliZ') {
                        // Z gate applies phase flip to |1⟩ on first qubit
                        currentState[2] = -currentState[2];
                        currentState[3] = -currentState[3];
                    }
                    updateDisplay();
                }
                
                function updateDisplay() {
                    const states = ['|00⟩', '|01⟩', '|10⟩', '|11⟩'];
                    let display = '<table><tr><th>State</th><th>Amplitude</th><th>Probability</th></tr>';
                    
                    for (let i = 0; i < 4; i++) {
                        const amp = currentState[i];
                        const prob = (amp * amp).toFixed(3);
                        const ampStr = amp.toFixed(3);
                        display += `<tr><td>${states[i]}</td><td>${ampStr}</td><td>${prob}</td></tr>`;
                    }
                    display += '</table>';
                    
                    document.getElementById('stateDisplay').innerHTML = display;
                    document.getElementById('result').style.display = 'block';
                }
                
                // Initialize
                resetState();
            </script>
        </body>
        </html>
    """
    return HttpResponse(html)


def app3(request):
    """Application 3: Dynamic Programming Example (Fibonacci with memoization)."""
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dynamic Programming Example</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                .info { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .comparison { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }
                .method { padding: 15px; border: 2px solid #ddd; border-radius: 5px; }
                .recursive { border-color: #f44336; }
                .dp { border-color: #4CAF50; }
                input { padding: 8px; margin: 5px; width: 100px; }
                button { padding: 10px 20px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer; }
                button:hover { background: #1976D2; }
                .result { margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 5px; }
                code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
            </style>
        </head>
        <body>
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
            
            <div>
                <h2>Calculate Fibonacci Number:</h2>
                <label>Enter n (0-40 recommended):</label><br>
                <input type="number" id="fibInput" value="10" min="0" max="40"><br>
                <button onclick="calculateFibonacci()">Calculate</button>
            </div>
            
            <div id="result" class="result" style="display:none;">
                <h3>Results:</h3>
                <div id="resultsDisplay"></div>
            </div>
            
            <div class="info">
                <h3>Fibonacci Sequence Definition:</h3>
                <p>F(0) = 0, F(1) = 1</p>
                <p>F(n) = F(n-1) + F(n-2) for n > 1</p>
                <p><strong>Example:</strong> 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...</p>
            </div>
            
            <script>
                // Memoization cache
                const memo = {};
                
                // Naive recursive (exponential time)
                function fibNaive(n) {
                    if (n <= 1) return n;
                    return fibNaive(n - 1) + fibNaive(n - 2);
                }
                
                // Dynamic Programming with memoization (linear time)
                function fibDP(n) {
                    if (n in memo) return memo[n];
                    if (n <= 1) {
                        memo[n] = n;
                        return n;
                    }
                    memo[n] = fibDP(n - 1) + fibDP(n - 2);
                    return memo[n];
                }
                
                // Tabulation (bottom-up approach)
                function fibTabulation(n) {
                    if (n <= 1) return n;
                    const dp = [0, 1];
                    for (let i = 2; i <= n; i++) {
                        dp[i] = dp[i - 1] + dp[i - 2];
                    }
                    return dp[n];
                }
                
                function calculateFibonacci() {
                    const n = parseInt(document.getElementById('fibInput').value);
                    
                    if (n < 0 || n > 40) {
                        alert('Please enter a number between 0 and 40');
                        return;
                    }
                    
                    // Clear memo for fresh calculation
                    Object.keys(memo).forEach(key => delete memo[key]);
                    
                    // Measure time for DP approach
                    const startDP = performance.now();
                    const resultDP = fibDP(n);
                    const timeDP = (performance.now() - startDP).toFixed(4);
                    
                    // Measure time for tabulation
                    const startTab = performance.now();
                    const resultTab = fibTabulation(n);
                    const timeTab = (performance.now() - startTab).toFixed(4);
                    
                    // Try naive approach for small n only
                    let resultNaive = 'N/A (too slow)';
                    let timeNaive = 'N/A';
                    if (n <= 30) {
                        const startNaive = performance.now();
                        resultNaive = fibNaive(n);
                        timeNaive = (performance.now() - startNaive).toFixed(4);
                    }
                    
                    const display = `
                        <p><strong>F(${n}) = ${resultDP}</strong></p>
                        <table border="1" style="border-collapse: collapse; width: 100%;">
                            <tr>
                                <th>Method</th>
                                <th>Result</th>
                                <th>Time (ms)</th>
                            </tr>
                            <tr>
                                <td>Dynamic Programming (Memoization)</td>
                                <td>${resultDP}</td>
                                <td>${timeDP}</td>
                            </tr>
                            <tr>
                                <td>Tabulation (Bottom-up)</td>
                                <td>${resultTab}</td>
                                <td>${timeTab}</td>
                            </tr>
                            <tr>
                                <td>Naive Recursive</td>
                                <td>${resultNaive}</td>
                                <td>${timeNaive}</td>
                            </tr>
                        </table>
                        <p><small>Note: Naive recursive approach is only calculated for n ≤ 30 due to exponential time complexity.</small></p>
                    `;
                    
                    document.getElementById('resultsDisplay').innerHTML = display;
                    document.getElementById('result').style.display = 'block';
                }
                
                // Calculate on load
                calculateFibonacci();
            </script>
        </body>
        </html>
    """
    return HttpResponse(html)
