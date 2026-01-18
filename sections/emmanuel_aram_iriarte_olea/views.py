from django.http import HttpResponse


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
                <li><a href="app1/">Application 1: LeetCode Problem (Two Sum)</a></li>
                <li><a href="app2/">Application 2: Basic Quantum Gates Simulator</a></li>
                <li><a href="app3/">Application 3: Dynamic Programming Example</a></li>
            </ul>
        </body>
        </html>
    """)


def app1(request):
    """Application 1: LeetCode Trapping Rain Water Problem (Hard)."""
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Trapping Rain Water - LeetCode Hard Problem</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
                .back-button { padding: 8px 15px; background: #666; color: white; text-decoration: none; border-radius: 4px; display: inline-block; margin-bottom: 20px; }
                .back-button:hover { background: #555; }
                .problem { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .example { background: #e8f4f8; padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; }
                code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
                input { padding: 8px; margin: 5px; width: 300px; }
                button { padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
                button:hover { background: #45a049; }
                #result { margin-top: 20px; padding: 15px; border-radius: 5px; display: none; }
                .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
                .visualization { margin: 20px 0; padding: 15px; background: #f9f9f9; border-radius: 5px; }
                .bar-container { display: flex; align-items: flex-end; justify-content: center; height: 300px; gap: 5px; margin: 20px 0; }
                .bar { background: #2196F3; width: 30px; border: 1px solid #1976D2; display: flex; flex-direction: column-reverse; }
                .water { background: #00BCD4; }
                .bar-label { text-align: center; margin-top: 5px; font-size: 12px; }
            </style>
        </head>
        <body>
            <a href="../" class="back-button">← Back to Index</a>
            <h1>LeetCode Problem: Trapping Rain Water (Hard)</h1>
            
            <div class="problem">
                <h2>Problem Description</h2>
                <p>Given <code>n</code> non-negative integers representing an elevation map where the width of each bar is 1, 
                compute how much water it can trap after raining.</p>
                <p><strong>Example:</strong></p>
                <p>Given elevation map <code>[0,1,0,2,1,0,1,3,2,1,2,1]</code>, return <code>6</code> units of water.</p>
            </div>
            
            <div class="example">
                <strong>Example 1:</strong><br>
                Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]<br>
                Output: 6<br>
                Explanation: The above elevation map is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. 
                In this case, 6 units of rain water (blue section) are being trapped.
            </div>
            
            <div class="example">
                <strong>Example 2:</strong><br>
                Input: height = [4,2,0,3,2,5]<br>
                Output: 9
            </div>
            
            <h2>Try it yourself:</h2>
            <div>
                <label>Height array (comma-separated non-negative integers):</label><br>
                <input type="text" id="heights" value="0,1,0,2,1,0,1,3,2,1,2,1" placeholder="0,1,0,2,1,0,1,3,2,1,2,1"><br>
                <button onclick="solveTrappingRainWater()">Solve</button>
            </div>
            
            <div id="result"></div>
            <div id="visualization" class="visualization" style="display:none;"></div>
            
            <script>
                function solveTrappingRainWater() {
                    const heightsStr = document.getElementById('heights').value;
                    
                    // Parse array
                    const height = heightsStr.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n) && n >= 0);
                    
                    if (height.length === 0) {
                        document.getElementById('result').innerHTML = 
                            '<strong>Error:</strong> Please enter valid non-negative integers.';
                        document.getElementById('result').style.display = 'block';
                        document.getElementById('result').className = 'success';
                        return;
                    }
                    
                    // Algorithm: Two Pointer Approach (O(n) time, O(1) space)
                    let left = 0, right = height.length - 1;
                    let leftMax = 0, rightMax = 0;
                    let water = 0;
                    
                    while (left < right) {
                        if (height[left] < height[right]) {
                            if (height[left] >= leftMax) {
                                leftMax = height[left];
                            } else {
                                water += leftMax - height[left];
                            }
                            left++;
                        } else {
                            if (height[right] >= rightMax) {
                                rightMax = height[right];
                            } else {
                                water += rightMax - height[right];
                            }
                            right--;
                        }
                    }
                    
                    // Create visualization
                    let maxHeight = Math.max(...height);
                    let visHTML = '<h3>Visualization:</h3><div class="bar-container">';
                    
                    for (let i = 0; i < height.length; i++) {
                        const barHeight = height[i];
                        const barPercent = (barHeight / maxHeight) * 100;
                        
                        // Calculate trapped water at this position (simplified for visualization)
                        let waterHeight = 0;
                        if (i > 0 && i < height.length - 1) {
                            const leftMaxHeight = Math.max(...height.slice(0, i));
                            const rightMaxHeight = Math.max(...height.slice(i + 1));
                            const minWall = Math.min(leftMaxHeight, rightMaxHeight);
                            if (minWall > barHeight) {
                                waterHeight = minWall - barHeight;
                            }
                        }
                        
                        const waterPercent = waterHeight > 0 ? (waterHeight / maxHeight) * 100 : 0;
                        
                        visHTML += '<div style="display: flex; flex-direction: column; align-items: center;">';
                        visHTML += `<div class="bar" style="height: ${barPercent}%;">`;
                        if (waterHeight > 0) {
                            visHTML += `<div class="water" style="height: ${waterPercent}%;"></div>`;
                        }
                        visHTML += '</div>';
                        visHTML += `<div class="bar-label">${barHeight}</div>`;
                        visHTML += '</div>';
                    }
                    visHTML += '</div>';
                    
                    document.getElementById('result').innerHTML = 
                        '<strong>Result:</strong> ' + water + ' units of trapped water<br>' +
                        '<strong>Input:</strong> [' + height.join(', ') + ']<br>' +
                        '<strong>Algorithm:</strong> Two-pointer approach (O(n) time, O(1) space)';
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('result').className = 'success';
                    
                    document.getElementById('visualization').innerHTML = visHTML;
                    document.getElementById('visualization').style.display = 'block';
                }
                
                // Auto-solve on load with default example
                window.onload = function() {
                    solveTrappingRainWater();
                };
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
                .back-button { padding: 8px 15px; background: #666; color: white; text-decoration: none; border-radius: 4px; display: inline-block; margin-bottom: 20px; }
                .back-button:hover { background: #555; }
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
            <a href="../" class="back-button">← Back to Index</a>
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
                .back-button { padding: 8px 15px; background: #666; color: white; text-decoration: none; border-radius: 4px; display: inline-block; margin-bottom: 20px; }
                .back-button:hover { background: #555; }
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
                    
                    // Try naive approach with 10 second timeout
                    let resultNaive = 'N/A (timeout or too slow)';
                    let timeNaive = 'N/A';
                    
                    // Use Promise with timeout for naive recursive
                    const naivePromise = new Promise((resolve) => {
                        const startNaive = performance.now();
                        try {
                            const result = fibNaive(n);
                            const elapsed = performance.now() - startNaive;
                            resolve({ result, elapsed });
                        } catch (e) {
                            resolve({ result: null, elapsed: null });
                        }
                    });
                    
                    // Wait up to 10 seconds (10000ms)
                    Promise.race([
                        naivePromise,
                        new Promise(resolve => setTimeout(() => resolve({ result: null, elapsed: null }), 10000))
                    ]).then(({ result, elapsed }) => {
                        if (result !== null && elapsed !== null) {
                            resultNaive = result;
                            timeNaive = elapsed.toFixed(4);
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
                                    <td>Naive Recursive (10s timeout)</td>
                                    <td>${resultNaive}</td>
                                    <td>${timeNaive}</td>
                                </tr>
                            </table>
                            <p><small>Note: Naive recursive approach has a 10-second timeout limit.</small></p>
                        `;
                        
                        document.getElementById('resultsDisplay').innerHTML = display;
                        document.getElementById('result').style.display = 'block';
                    });
                }
                
                // Calculate on load
                calculateFibonacci();
            </script>
        </body>
        </html>
    """
    return HttpResponse(html)
