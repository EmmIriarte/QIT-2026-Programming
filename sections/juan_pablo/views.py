import json
from django.http import HttpResponse


# =============================================================================
# APPLICATION 1 DATA: SUDOKU VALIDATOR
# =============================================================================

EXAMPLE_BOARDS = {
    'valid': [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ],
    'invalid_row': [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        ["9","9",".",".","8",".",".","7","."]
    ],
    'invalid_column': [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        ["5",".",".",".",".",".",".","7","9"]
    ],
}


# =============================================================================
# APPLICATION 2 DATA: MULTI-THREADED PROGRAMMING
# =============================================================================

MULTITHREADING_DATA = {
    'fundamentals': {
        'title': 'Fundamentals of Multi-Threading',
        'description': 'Multi-threaded programming allows a program to execute multiple threads concurrently within a single process. Each thread shares the same memory space but runs independently, enabling parallelism and better resource utilization.',
        'content': [
            {
                'subtitle': 'What is a Thread?',
                'text': 'A thread is the smallest unit of execution within a process. While a process has its own memory space, threads within the same process share memory (heap) but each has its own stack. This shared memory model makes threads lightweight compared to processes, but introduces complexity around data access.'
            },
            {
                'subtitle': 'Threads vs Processes',
                'text': 'Processes are isolated with separate memory spaces and communicate via IPC (pipes, sockets, shared memory). Threads share the same address space within a process, making communication faster but requiring synchronization. Creating a thread is cheaper than creating a process. In Python, the multiprocessing module creates processes, while the threading module creates threads.'
            },
            {
                'subtitle': 'Concurrency vs Parallelism',
                'text': 'Concurrency means multiple tasks make progress over time (possibly interleaved on one core). Parallelism means tasks literally execute at the same instant on multiple cores. Multi-threading enables concurrency; true parallelism depends on the hardware and runtime. A single-core CPU can run concurrent threads but not parallel ones.'
            },
            {
                'subtitle': 'Why Use Multi-Threading?',
                'text': 'Multi-threading improves responsiveness (e.g., keeping a UI responsive while performing background work), utilizes multi-core CPUs for computation, and handles I/O-bound tasks efficiently (e.g., downloading multiple files simultaneously). Web servers use thread pools to handle many client requests concurrently.'
            },
        ],
        'key_concepts': ['Thread', 'Process', 'Concurrency', 'Parallelism', 'Shared Memory', 'Stack vs Heap'],
    },
    'synchronization': {
        'title': 'Synchronization Mechanisms',
        'description': 'When multiple threads access shared data, synchronization mechanisms are needed to prevent data corruption and ensure correctness. Without proper synchronization, programs can produce unpredictable and incorrect results.',
        'content': [
            {
                'subtitle': 'Mutex (Mutual Exclusion Lock)',
                'text': 'A mutex ensures that only one thread can access a critical section at a time. A thread must acquire the lock before entering and release it when done. If the lock is held by another thread, the requesting thread blocks until it becomes available. In Python: threading.Lock(). Misuse can lead to deadlocks if locks are not released properly.'
            },
            {
                'subtitle': 'Semaphore',
                'text': 'A semaphore is a generalized mutex that allows a fixed number of threads to access a resource simultaneously. A counting semaphore with value N permits N threads to hold it concurrently. A binary semaphore (value 1) behaves like a mutex. Common use case: limiting concurrent database connections to a pool of N. In Python: threading.Semaphore(N).'
            },
            {
                'subtitle': 'Condition Variables',
                'text': 'Condition variables allow threads to wait for a specific condition to become true before proceeding. A thread can call wait() to block until another thread signals the condition with notify() or notify_all(). Classic example: producer-consumer pattern where the consumer waits until the producer adds an item to the buffer. In Python: threading.Condition().'
            },
            {
                'subtitle': 'Read-Write Locks',
                'text': 'Read-write locks allow multiple threads to read shared data simultaneously, but only one thread can write at a time. When a writer holds the lock, all readers and other writers are blocked. This improves performance when reads are much more frequent than writes, such as in caching systems or configuration lookups.'
            },
        ],
        'key_concepts': ['Mutex', 'Semaphore', 'Condition Variable', 'Critical Section', 'Read-Write Lock', 'Blocking'],
    },
    'problems': {
        'title': 'Common Multi-Threading Problems',
        'description': 'Multi-threaded programs are prone to subtle bugs that are difficult to reproduce and debug. Understanding these problems is essential to writing correct concurrent code.',
        'content': [
            {
                'subtitle': 'Race Conditions',
                'text': 'A race condition occurs when the behavior of a program depends on the relative timing of thread execution. For example, if two threads both read a counter value of 5, increment it, and write 6, one increment is lost. The result depends on which thread executes first. Solution: use locks to make the read-modify-write operation atomic.'
            },
            {
                'subtitle': 'Deadlocks',
                'text': 'A deadlock occurs when two or more threads are waiting for each other to release resources, and none can proceed. Classic example: Thread A holds Lock 1 and waits for Lock 2, while Thread B holds Lock 2 and waits for Lock 1. Four conditions must hold simultaneously for deadlock: mutual exclusion, hold and wait, no preemption, and circular wait. Prevention strategies include lock ordering and timeout-based acquisition.'
            },
            {
                'subtitle': 'Starvation',
                'text': 'Starvation occurs when a thread is perpetually denied access to a resource because other threads keep acquiring it first. For example, if high-priority threads always run before low-priority ones, the low-priority thread may never execute. Fair locks and priority aging are common solutions to prevent starvation.'
            },
            {
                'subtitle': 'Livelock',
                'text': 'A livelock is similar to a deadlock, but threads are not blocked - they keep changing state in response to each other without making progress. Imagine two people in a hallway who keep stepping aside in the same direction to let the other pass. Both are active but neither moves forward. Adding randomized delays or backoff strategies can resolve livelocks.'
            },
        ],
        'key_concepts': ['Race Condition', 'Deadlock', 'Starvation', 'Livelock', 'Atomic Operation', 'Lock Ordering'],
    },
    'python': {
        'title': 'Multi-Threading in Python',
        'description': 'Python provides built-in modules for multi-threaded programming, but has unique characteristics due to the Global Interpreter Lock (GIL) that affect how threads execute.',
        'content': [
            {
                'subtitle': 'The Global Interpreter Lock (GIL)',
                'text': 'CPython (the standard Python interpreter) has a GIL that allows only one thread to execute Python bytecode at a time. This means CPU-bound Python threads do not achieve true parallelism. However, the GIL is released during I/O operations (file reads, network calls), so I/O-bound programs benefit significantly from threading. For CPU-bound parallelism, use the multiprocessing module instead.'
            },
            {
                'subtitle': 'The threading Module',
                'text': 'Python\'s threading module provides Thread objects, Locks, Semaphores, Events, and Conditions. Basic usage: create a Thread with a target function, call start() to begin execution, and join() to wait for completion. Example: t = threading.Thread(target=my_func, args=(arg1,)); t.start(); t.join(). Daemon threads are background threads that exit when the main program exits.'
            },
            {
                'subtitle': 'concurrent.futures Module',
                'text': 'The concurrent.futures module provides a high-level interface for asynchronous execution. ThreadPoolExecutor manages a pool of threads and returns Future objects representing pending results. Usage: with ThreadPoolExecutor(max_workers=4) as executor: future = executor.submit(func, arg). The map() method applies a function to an iterable in parallel. This is the recommended approach for most threading tasks in Python.'
            },
            {
                'subtitle': 'Thread-Safe Data Structures',
                'text': 'Python\'s queue.Queue is a thread-safe FIFO queue designed for producer-consumer scenarios. It handles all locking internally. Methods: put() adds an item (blocks if full), get() removes an item (blocks if empty), task_done() signals completion. Other thread-safe operations: list.append() and dict operations are atomic in CPython due to the GIL, but relying on this is not recommended for portable code.'
            },
        ],
        'key_concepts': ['GIL', 'threading Module', 'ThreadPoolExecutor', 'Future', 'Daemon Thread', 'queue.Queue'],
    },
}


# =============================================================================
# APPLICATION 3 DATA: GRAPHENE PRESENTATION
# =============================================================================

GRAPHENE_DATA = {
    'what-is': {
        'title': 'What is Graphene?',
        'order': 1,
        'content': 'Graphene is a single layer of carbon atoms arranged in a two-dimensional hexagonal lattice structure, resembling a honeycomb pattern. It was first successfully isolated in 2004 by Andre Geim and Konstantin Novoselov at the University of Manchester, who received the Nobel Prize in Physics in 2010 for their groundbreaking work.\n\nGraphene is often called a "wonder material" because of its extraordinary combination of properties. Despite being only one atom thick (the thinnest material known), it is one of the strongest materials ever tested - approximately 200 times stronger than steel while being incredibly lightweight.',
        'key_properties': [
            'Strongest material known (130 GPa tensile strength, 200x stronger than steel)',
            'Superior electrical conductivity (better than copper)',
            'Capable of superconductivity',
            'Ultra-thin (one atom thick), transparent, and flexible',
            'UV resistant',
            'High electron mobility (200,000 cm2/Vs)',
            'Impermeable to gases',
            'Excellent nano-enhancer properties',
        ],
    },
    'applications': {
        'title': 'Applications of Graphene',
        'order': 2,
        'content': 'Graphene\'s unique combination of properties enables numerous applications across various industries. While many applications are still in research or early commercialization phases, graphene-enhanced products are already appearing in the market.',
        'categories': [
            {
                'name': 'Electronics & Semiconductors',
                'items': ['Ultra-fast transistors', '5G technology components', 'Flexible touchscreens', 'Wearable sensors', 'Quantum computers'],
            },
            {
                'name': 'Energy Storage',
                'items': ['Enhanced batteries (faster charging, higher capacity)', 'Supercapacitors', 'Superconductivity applications', 'Solar cell improvements'],
            },
            {
                'name': 'Construction',
                'items': ['Enhanced concrete (40% stronger)', 'Anti-corrosion coatings', 'Structural composites'],
            },
            {
                'name': 'Water Treatment',
                'items': ['Desalination membranes', 'Oil-water separation', 'Waste water filtration', 'Contaminant removal'],
            },
            {
                'name': 'Aerospace & Automotive',
                'items': ['Lightweight composites', 'Thermal regulation systems', 'De-icing coatings', 'Fuel efficiency improvements'],
            },
            {
                'name': 'Medical & Biotech',
                'items': ['Biosensors', 'Drug delivery systems', 'Neural interfaces', 'Antibacterial coatings', 'Tissue engineering'],
            },
            {
                'name': 'Textiles',
                'items': ['Smart clothing', 'Thermal regulation fabrics', 'Antibacterial fabrics', 'Conductive textiles'],
            },
        ],
    },
    'types': {
        'title': 'Types of Graphene',
        'order': 3,
        'content': 'Different types of graphene exist, varying in layer count, production method, and price. The quality and properties depend on the production method used.',
        'types_table': [
            {'name': 'Monolayer Graphene', 'price': '$500 - $5,000/gram', 'use_cases': 'Research, high-performance electronics, sensors'},
            {'name': 'Few-layer Graphene', 'price': '$100 - $500/gram', 'use_cases': 'Electronics, composites, coatings'},
            {'name': 'Graphene Oxide (GO)', 'price': '$18.25 - $200/gram', 'use_cases': 'Water filtration, biomedical applications, composites'},
            {'name': 'Reduced Graphene Oxide (rGO)', 'price': '$50 - $60/gram', 'use_cases': 'Energy storage, conductive inks, sensors'},
            {'name': 'Graphene Nanoplatelets', 'price': '$0.05 - $0.09/gram', 'use_cases': 'Composites, coatings, lubricants, bulk applications'},
            {'name': 'Flash Graphene', 'price': '$0.0738 - $0.22/gram', 'use_cases': 'Large-scale applications, concrete enhancement, bulk materials'},
        ],
    },
    'production': {
        'title': 'Production Methods',
        'order': 4,
        'content': 'Several methods exist for producing graphene, each with different trade-offs between quality, scalability, and cost.',
        'methods': [
            {
                'name': 'Mechanical Exfoliation (Scotch Tape Method)',
                'description': 'The original method used by Geim and Novoselov. Uses adhesive tape to peel layers from graphite.',
                'quality': 'Pristine (highest)',
                'scalability': 'Lab use only',
                'cost': 'Low setup cost',
                'output': 'Very small quantities',
            },
            {
                'name': 'Liquid-Phase Exfoliation (LPE)',
                'description': 'Graphite is sonicated in a solvent to separate layers into graphene flakes.',
                'quality': 'Good',
                'scalability': 'High',
                'cost': '$50K - $500K setup',
                'output': '~20g/hour',
            },
            {
                'name': 'Chemical Vapor Deposition (CVD)',
                'description': 'Carbon atoms are deposited on a metal substrate from a gas phase at high temperatures.',
                'quality': 'High',
                'scalability': 'Medium',
                'cost': '$500K - $3M setup',
                'output': 'Large area films',
            },
            {
                'name': 'Graphene Oxide Reduction',
                'description': 'Graphite is oxidized to graphene oxide, then chemically or thermally reduced.',
                'quality': 'Moderate (defects present)',
                'scalability': 'High',
                'cost': '$100K - $300K setup',
                'output': 'Bulk quantities',
            },
            {
                'name': 'Thermal Exfoliation',
                'description': 'Rapid heating causes graphite layers to separate due to thermal expansion.',
                'quality': 'Moderate',
                'scalability': 'High',
                'cost': '$300K - $1M setup',
                'output': 'Industrial scale',
            },
            {
                'name': 'Epitaxial Growth on SiC',
                'description': 'Graphene grows on silicon carbide substrates through thermal decomposition.',
                'quality': 'Highest',
                'scalability': 'Low',
                'cost': '$1M - $5M setup',
                'output': 'Wafer-scale films',
            },
        ],
    },
    'adoption': {
        'title': 'Why Limited Adoption?',
        'order': 5,
        'content': 'Despite graphene\'s remarkable properties and potential, widespread commercial adoption has been slower than initially expected. Understanding these barriers helps explain the current state of graphene commercialization.',
        'barriers': [
            {
                'title': 'High Production Costs',
                'description': 'High-quality graphene remains expensive to produce at scale. The cost-performance ratio often doesn\'t justify replacement of existing materials.',
            },
            {
                'title': 'Quality vs. Scalability Trade-off',
                'description': 'Methods that produce the highest quality graphene (CVD, epitaxial growth) are expensive and hard to scale. Scalable methods produce lower quality material.',
            },
            {
                'title': 'Lack of Global Standards',
                'description': 'No universal standards exist for graphene quality, making it difficult for buyers to compare products from different suppliers.',
            },
            {
                'title': 'Manufacturing Integration',
                'description': 'Existing manufacturing processes weren\'t designed for graphene. Integration requires significant R&D and capital investment.',
            },
            {
                'title': 'No "Killer Application"',
                'description': 'While graphene improves many things incrementally, no single application has emerged where graphene is irreplaceable.',
            },
            {
                'title': 'Fragmented Industry',
                'description': 'The graphene industry consists of many small companies with limited resources for large-scale commercialization.',
            },
        ],
        'why_start_now': [
            'Market maturity: Industry has moved past hype to realistic applications',
            'Declining costs: Production costs have dropped significantly since 2010',
            'Growing demand: Major industries actively seeking graphene solutions',
            'Funding availability: Increased government and private investment',
            'Established supply chains: Reliable suppliers now exist',
        ],
    },
}


# =============================================================================
# VIEW FUNCTIONS
# =============================================================================

def index(request):
    """Student index page displaying name and three application links."""
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Juan Pablo Sanchez - QIT 2026 Programming</title>
        </head>
        <body>
            <h1>Juan Pablo Sanchez</h1>
            <ul>
                <li><a href="app1/">Application 1: Sudoku Validator</a></li>
                <li><a href="app2/">Application 2: Multi-Threaded Programming</a></li>
                <li><a href="app3/">Application 3: Graphene Presentation</a></li>
            </ul>
        </body>
        </html>
    """)


SUDOKU_STYLE = """
<style>
    body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
    .board-table { border-collapse: collapse; margin: 20px 0; }
    .board-table td { border: 1px solid #333; width: 40px; height: 40px; text-align: center; font-size: 18px; font-weight: bold; }
    .board-table tr:nth-child(3n) td { border-bottom: 3px solid #000; }
    .board-table td:nth-child(3n) { border-right: 3px solid #000; }
    .board-table tr:first-child td { border-top: 3px solid #000; }
    .board-table td:first-child { border-left: 3px solid #000; }
    .board-table td.empty { color: #ccc; }
    .valid { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; border-radius: 5px; }
    .invalid { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 15px; border-radius: 5px; }
    .board-selector a, .board-selector button { display: inline-block; padding: 8px 16px; margin: 5px; background: #2196F3; color: white; text-decoration: none; border-radius: 4px; border: none; cursor: pointer; font-size: 14px; }
    .board-selector a:hover, .board-selector button:hover { background: #1976D2; }
    .board-selector button.active { background: #1976D2; font-weight: bold; }
    .info { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
    pre { background: #f0f0f0; padding: 15px; border-radius: 5px; overflow-x: auto; }
    table.analysis { border-collapse: collapse; width: 100%; margin: 10px 0; }
    table.analysis td { border: 1px solid #ddd; padding: 8px; }
    .box-diagram td { border: 1px solid #333; width: 120px; height: 60px; text-align: center; font-size: 14px; }
</style>
"""


def app1(request):
    """Application 1: Sudoku Validator"""
    boards_json = json.dumps(EXAMPLE_BOARDS)
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sudoku Validator - Juan Pablo Sanchez</title>
            """ + SUDOKU_STYLE + """
        </head>
        <body>
            <p><a href="/juan_pablo/">Back to Home</a></p>
            <h1>Sudoku Validator</h1>
            <p>LeetCode Problem #36 - Validate a 9x9 Sudoku board</p>

            <h3>Current Board: <span id="board-label">Valid</span></h3>
            <table class="board-table" id="board-table"></table>

            <div class="board-selector">
                <strong>Select a board:</strong><br>
                <button type="button" data-board="valid">Valid</button>
                <button type="button" data-board="invalid_row">Invalid Row</button>
                <button type="button" data-board="invalid_column">Invalid Column</button>
            </div>

            <h3>Validation Result</h3>
            <div id="result-box" class="valid">
                <strong id="result-status">VALID</strong>
                <p id="result-message"></p>
            </div>

            <div class="info">
                <h3>Sudoku Rules</h3>
                <p>A valid Sudoku board must satisfy:</p>
                <ul>
                    <li>Each row contains digits 1-9 without repetition</li>
                    <li>Each column contains digits 1-9 without repetition</li>
                    <li>Each 3x3 sub-box contains digits 1-9 without repetition</li>
                    <li>Empty cells (marked with '.') are allowed</li>
                </ul>
            </div>

            <div class="info">
                <h2>Algorithm Explanation</h2>
                <p>The algorithm validates the board in <strong>three separate passes</strong>, each checking one constraint using a Set to detect duplicates:</p>
                <h3>Pass 1 &mdash; Rows</h3>
                <p>For each row, a Set tracks digits seen; duplicate in row &rarr; invalid.</p>
                <h3>Pass 2 &mdash; Columns</h3>
                <p>Same logic with indices swapped (<code>board[j][i]</code>).</p>
                <h3>Pass 3 &mdash; 3x3 Boxes</h3>
                <p>Nine top-left corners; scan each 3&times;3 box with a Set.</p>
            </div>

            <div class="info">
                <h2>Complexity</h2>
                <table class="analysis">
                    <tr><td><strong>Time</strong></td><td>O(n&sup2;), n=9</td></tr>
                    <tr><td><strong>Space</strong></td><td>O(n), one Set per group</td></tr>
                </table>
            </div>

            <script>
            (function() {
                var exampleBoards = """ + boards_json + """;

                function isValidSudoku(board) {
                    var i, j, item, seen, startRow, startCol, row, col, boxNumRow, boxNumCol;
                    // Pass 1: rows
                    for (i = 0; i < 9; i++) {
                        seen = new Set();
                        for (j = 0; j < 9; j++) {
                            item = board[i][j];
                            if (seen.has(item)) return { valid: false, message: "Duplicate '" + item + "' found in row " + (i + 1) };
                            if (item !== '.') seen.add(item);
                        }
                    }
                    // Pass 2: columns
                    for (i = 0; i < 9; i++) {
                        seen = new Set();
                        for (j = 0; j < 9; j++) {
                            item = board[j][i];
                            if (seen.has(item)) return { valid: false, message: "Duplicate '" + item + "' found in column " + (i + 1) };
                            if (item !== '.') seen.add(item);
                        }
                    }
                    // Pass 3: 3x3 boxes
                    var boxStarts = [[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]];
                    for (var b = 0; b < boxStarts.length; b++) {
                        startRow = boxStarts[b][0]; startCol = boxStarts[b][1];
                        seen = new Set();
                        for (row = startRow; row < startRow + 3; row++) {
                            for (col = startCol; col < startCol + 3; col++) {
                                item = board[row][col];
                                if (seen.has(item)) {
                                    boxNumRow = Math.floor(startRow / 3) + 1;
                                    boxNumCol = Math.floor(startCol / 3) + 1;
                                    return { valid: false, message: "Duplicate '" + item + "' found in 3x3 box (" + boxNumRow + ", " + boxNumCol + ")" };
                                }
                                if (item !== '.') seen.add(item);
                            }
                        }
                    }
                    return { valid: true, message: "Valid Sudoku board! No duplicates found in any row, column, or 3x3 box." };
                }

                function renderBoard(board) {
                    var table = document.getElementById('board-table');
                    table.innerHTML = '';
                    for (var r = 0; r < 9; r++) {
                        var tr = document.createElement('tr');
                        for (var c = 0; c < 9; c++) {
                            var td = document.createElement('td');
                            td.textContent = board[r][c];
                            if (board[r][c] === '.') td.className = 'empty';
                            tr.appendChild(td);
                        }
                        table.appendChild(tr);
                    }
                }

                function updateResult() {
                    var sel = document.querySelector('.board-selector button[data-board].active') || document.querySelector('.board-selector button[data-board]');
                    var boardKey = sel ? sel.getAttribute('data-board') : 'valid';
                    if (!exampleBoards[boardKey]) boardKey = 'valid';
                    document.querySelectorAll('.board-selector button[data-board]').forEach(function(btn) {
                        btn.classList.toggle('active', btn.getAttribute('data-board') === boardKey);
                    });
                    var label = document.getElementById('board-label');
                    label.textContent = boardKey.replace(/_/g, ' ').replace(/\\b\\w/g, function(c) { return c.toUpperCase(); });
                    var board = exampleBoards[boardKey];
                    renderBoard(board);
                    var result = isValidSudoku(board);
                    var box = document.getElementById('result-box');
                    box.className = result.valid ? 'valid' : 'invalid';
                    document.getElementById('result-status').textContent = result.valid ? 'VALID' : 'INVALID';
                    document.getElementById('result-message').textContent = result.message;
                }

                document.querySelectorAll('.board-selector button[data-board]').forEach(function(btn) {
                    btn.addEventListener('click', function() {
                        var key = this.getAttribute('data-board');
                        document.querySelectorAll('.board-selector button[data-board]').forEach(function(b) { b.classList.remove('active'); });
                        this.classList.add('active');
                        document.getElementById('board-label').textContent = key.replace(/_/g, ' ').replace(/\\b\\w/g, function(c) { return c.toUpperCase(); });
                        renderBoard(exampleBoards[key]);
                        var result = isValidSudoku(exampleBoards[key]);
                        document.getElementById('result-box').className = result.valid ? 'valid' : 'invalid';
                        document.getElementById('result-status').textContent = result.valid ? 'VALID' : 'INVALID';
                        document.getElementById('result-message').textContent = result.message;
                    });
                });

                updateResult();
            })();
            </script>
        </body>
        </html>
    """
    return HttpResponse(html)


THREADING_STYLE = """
<style>
    body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
    .toc { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
    .toc a { display: inline-block; padding: 5px 12px; margin: 3px; background: #7B1FA2; color: white; text-decoration: none; border-radius: 4px; }
    .toc a:hover { background: #6A1B9A; }
    .topic { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
    .topic h2 { color: #6A1B9A; border-bottom: 2px solid #7B1FA2; padding-bottom: 10px; }
    .key-concepts { background: #F3E5F5; padding: 10px 15px; border-radius: 5px; margin: 10px 0; }
    .key-concepts span { display: inline-block; background: #7B1FA2; color: white; padding: 3px 10px; margin: 3px; border-radius: 12px; font-size: 14px; }
    .subsection { margin: 15px 0; padding: 10px; border-left: 4px solid #7B1FA2; background: #fafafa; }
    .subsection h4 { margin-top: 0; }
    hr { border: none; border-top: 1px solid #eee; margin: 30px 0; }
</style>
"""


def app2(request):
    """Application 2: Multi-Threaded Programming"""
    data_json = json.dumps(MULTITHREADING_DATA)
    # Escape </script> in JSON so it doesn't break the script tag
    data_json_escaped = data_json.replace("</", "<\\/")
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Multi-Threaded Programming - Juan Pablo Sanchez</title>
            """ + THREADING_STYLE + """
        </head>
        <body>
            <p><a href="/juan_pablo/">Back to Home</a></p>
            <h1>Multi-Threaded Programming</h1>
            <p>Understanding concurrency, synchronization, and parallel execution in software</p>

            <div class="toc" id="toc"><strong>Topics:</strong><br></div>
            <div id="topics"></div>

            <script>
            (function() {
                var data = """ + data_json_escaped + """;
                var toc = document.getElementById('toc');
                var topicsEl = document.getElementById('topics');
                for (var topicId in data) {
                    if (!data.hasOwnProperty(topicId)) continue;
                    var topic = data[topicId];
                    var a = document.createElement('a');
                    a.href = '#' + topicId;
                    a.textContent = topic.title;
                    toc.appendChild(a);
                    toc.appendChild(document.createTextNode(' '));

                    var div = document.createElement('div');
                    div.className = 'topic';
                    div.id = topicId;
                    div.innerHTML = '<h2>' + topic.title + '</h2><p>' + topic.description + '</p>';
                    var conceptsDiv = document.createElement('div');
                    conceptsDiv.className = 'key-concepts';
                    conceptsDiv.innerHTML = '<strong>Key Concepts:</strong><br>';
                    for (var k = 0; k < topic.key_concepts.length; k++) {
                        var span = document.createElement('span');
                        span.textContent = topic.key_concepts[k];
                        conceptsDiv.appendChild(span);
                        conceptsDiv.appendChild(document.createTextNode(' '));
                    }
                    div.appendChild(conceptsDiv);
                    for (var c = 0; c < topic.content.length; c++) {
                        var sec = topic.content[c];
                        var sub = document.createElement('div');
                        sub.className = 'subsection';
                        sub.innerHTML = '<h4>' + sec.subtitle + '</h4><p>' + sec.text + '</p>';
                        div.appendChild(sub);
                    }
                    topicsEl.appendChild(div);
                }
            })();
            </script>
        </body>
        </html>
    """
    return HttpResponse(html)


GRAPHENE_STYLE = """
<style>
    body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
    .toc { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
    .toc a { display: inline-block; padding: 5px 12px; margin: 3px; background: #4CAF50; color: white; text-decoration: none; border-radius: 4px; }
    .toc a:hover { background: #388E3C; }
    .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
    .section h2 { color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
    table { border-collapse: collapse; width: 100%; margin: 10px 0; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #4CAF50; color: white; }
    .category { margin: 10px 0; padding: 10px; background: #f9f9f9; border-left: 4px solid #4CAF50; }
    .category h4 { margin-top: 0; color: #2E7D32; }
    .method { margin: 10px 0; padding: 10px; background: #f9f9f9; border-left: 4px solid #4CAF50; }
    .method h4 { margin-top: 0; }
    .barrier { margin: 10px 0; padding: 10px; background: #fff3e0; border-left: 4px solid #FF9800; }
    .barrier h4 { margin-top: 0; color: #E65100; }
    .props li { margin: 5px 0; }
    .quick-facts span { display: inline-block; background: #4CAF50; color: white; padding: 8px 16px; margin: 5px; border-radius: 4px; font-weight: bold; }
    hr { border: none; border-top: 1px solid #eee; margin: 30px 0; }
</style>
"""


def app3(request):
    """Application 3: Graphene Presentation"""
    data_json = json.dumps(GRAPHENE_DATA)
    data_json_escaped = data_json.replace("</", "<\\/")
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Graphene Presentation - Juan Pablo Sanchez</title>
            """ + GRAPHENE_STYLE + """
        </head>
        <body>
            <p><a href="/juan_pablo/">Back to Home</a></p>
            <h1>Graphene: The Wonder Material</h1>
            <p>Discover the revolutionary material that could transform technology, energy, and manufacturing</p>

            <div class="quick-facts">
                <span>200x Stronger than steel</span>
                <span>Discovered 2004</span>
                <span>1 atom thick</span>
            </div>

            <div class="toc" id="toc"><strong>Sections:</strong><br></div>
            <div id="sections"></div>

            <script>
            (function() {
                var data = """ + data_json_escaped + """;
                var keys = Object.keys(data);
                keys.sort(function(a, b) { return data[a].order - data[b].order; });

                var toc = document.getElementById('toc');
                var sectionsEl = document.getElementById('sections');

                for (var i = 0; i < keys.length; i++) {
                    var sectionId = keys[i];
                    var section = data[sectionId];
                    var a = document.createElement('a');
                    a.href = '#' + sectionId;
                    a.textContent = section.order + '. ' + section.title;
                    toc.appendChild(a);
                    toc.appendChild(document.createTextNode(' '));

                    var div = document.createElement('div');
                    div.className = 'section';
                    div.id = sectionId;
                    div.innerHTML = '<h2>' + section.order + '. ' + section.title + '</h2>';

                    var paras = section.content.split(/\\n\\n/);
                    for (var p = 0; p < paras.length; p++) {
                        if (paras[p].trim()) {
                            var paraEl = document.createElement('p');
                            paraEl.textContent = paras[p].trim();
                            div.appendChild(paraEl);
                        }
                    }

                    if (section.key_properties) {
                        var h3 = document.createElement('h3');
                        h3.textContent = 'Key Properties';
                        div.appendChild(h3);
                        var ul = document.createElement('ul');
                        ul.className = 'props';
                        for (var k = 0; k < section.key_properties.length; k++) {
                            var li = document.createElement('li');
                            li.textContent = section.key_properties[k];
                            ul.appendChild(li);
                        }
                        div.appendChild(ul);
                    }

                    if (section.categories) {
                        var catH3 = document.createElement('h3');
                        catH3.textContent = 'Applications by Category';
                        div.appendChild(catH3);
                        for (var c = 0; c < section.categories.length; c++) {
                            var cat = section.categories[c];
                            var catDiv = document.createElement('div');
                            catDiv.className = 'category';
                            catDiv.innerHTML = '<h4>' + cat.name + '</h4>';
                            var catUl = document.createElement('ul');
                            for (var it = 0; it < cat.items.length; it++) {
                                var catLi = document.createElement('li');
                                catLi.textContent = cat.items[it];
                                catUl.appendChild(catLi);
                            }
                            catDiv.appendChild(catUl);
                            div.appendChild(catDiv);
                        }
                    }

                    if (section.types_table) {
                        var th3 = document.createElement('h3');
                        th3.textContent = 'Types and Pricing';
                        div.appendChild(th3);
                        var table = document.createElement('table');
                        table.innerHTML = '<thead><tr><th>Type</th><th>Price Range</th><th>Use Cases</th></tr></thead><tbody></tbody>';
                        var tbody = table.querySelector('tbody');
                        for (var t = 0; t < section.types_table.length; t++) {
                            var row = section.types_table[t];
                            var tr = document.createElement('tr');
                            tr.innerHTML = '<td><strong>' + row.name + '</strong></td><td>' + row.price + '</td><td>' + row.use_cases + '</td>';
                            tbody.appendChild(tr);
                        }
                        div.appendChild(table);
                    }

                    if (section.methods) {
                        var mH3 = document.createElement('h3');
                        mH3.textContent = 'Production Methods Comparison';
                        div.appendChild(mH3);
                        for (var m = 0; m < section.methods.length; m++) {
                            var method = section.methods[m];
                            var mDiv = document.createElement('div');
                            mDiv.className = 'method';
                            mDiv.innerHTML = '<h4>' + method.name + '</h4><p>' + method.description + '</p><ul><li><strong>Quality:</strong> ' + method.quality + '</li><li><strong>Scalability:</strong> ' + method.scalability + '</li><li><strong>Setup Cost:</strong> ' + method.cost + '</li><li><strong>Output:</strong> ' + method.output + '</li></ul>';
                            div.appendChild(mDiv);
                        }
                    }

                    if (section.barriers) {
                        var bH3 = document.createElement('h3');
                        bH3.textContent = 'Adoption Barriers';
                        div.appendChild(bH3);
                        for (var b = 0; b < section.barriers.length; b++) {
                            var barrier = section.barriers[b];
                            var bDiv = document.createElement('div');
                            bDiv.className = 'barrier';
                            bDiv.innerHTML = '<h4>' + barrier.title + '</h4><p>' + barrier.description + '</p>';
                            div.appendChild(bDiv);
                        }
                    }

                    if (section.why_start_now) {
                        var wH3 = document.createElement('h3');
                        wH3.textContent = 'Why Start Now?';
                        div.appendChild(wH3);
                        var wUl = document.createElement('ul');
                        for (var w = 0; w < section.why_start_now.length; w++) {
                            var li = document.createElement('li');
                            li.textContent = section.why_start_now[w];
                            wUl.appendChild(li);
                        }
                        div.appendChild(wUl);
                    }

                    sectionsEl.appendChild(div);
                }
            })();
            </script>
        </body>
        </html>
    """
    return HttpResponse(html)
