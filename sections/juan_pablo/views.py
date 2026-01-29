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


def is_valid_sudoku(board):
    """
    Determines whether a 9x9 Sudoku board is valid.

    A board is valid when no digit (1-9) appears more than once in any
    row, any column, or any of the nine 3x3 sub-boxes. Empty cells,
    represented by '.', are ignored during validation.

    The algorithm performs three independent validation passes:
      1. Row check   – iterate across each row looking for duplicate digits.
      2. Column check – iterate down each column looking for duplicate digits.
      3. Box check   – iterate through each 3x3 sub-box looking for duplicates.

    Each pass uses a fresh set per group. If a digit is already in the set
    the board is invalid; otherwise the digit is added to the set.

    Args:
        board: A 9x9 list of lists containing single-character strings
               ('1'-'9' for filled cells, '.' for empty cells).

    Returns:
        A tuple (is_valid: bool, message: str) describing the result.

    Time Complexity:  O(n^2) where n = 9 (three passes over the 81 cells).
    Space Complexity: O(n)   (at most 9 elements stored per set at a time).
    """

    # --- Pass 1: validate every row -------------------------------------------
    # Walk each row left-to-right; a set tracks digits seen so far in that row.
    for i in range(9):
        seen = set()
        for j in range(9):
            item = board[i][j]
            if item in seen:
                return False, f"Duplicate '{item}' found in row {i + 1}"
            elif item != '.':
                seen.add(item)

    # --- Pass 2: validate every column ----------------------------------------
    # Walk each column top-to-bottom; note the swapped indices board[j][i].
    for i in range(9):
        seen = set()
        for j in range(9):
            item = board[j][i]
            if item in seen:
                return False, f"Duplicate '{item}' found in column {i + 1}"
            elif item != '.':
                seen.add(item)

    # --- Pass 3: validate every 3x3 sub-box -----------------------------------
    # Each box is identified by the (row, col) of its top-left corner.
    # We enumerate all nine starting positions explicitly for clarity.
    box_starts = [
        (0, 0), (0, 3), (0, 6),
        (3, 0), (3, 3), (3, 6),
        (6, 0), (6, 3), (6, 6),
    ]

    for start_row, start_col in box_starts:
        seen = set()
        # Scan the 3 rows and 3 columns that belong to this box.
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                item = board[row][col]
                if item in seen:
                    box_num_row = (start_row // 3) + 1
                    box_num_col = (start_col // 3) + 1
                    return False, f"Duplicate '{item}' found in 3x3 box ({box_num_row}, {box_num_col})"
                elif item != '.':
                    seen.add(item)

    return True, "Valid Sudoku board! No duplicates found in any row, column, or 3x3 box."


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
    'patterns': {
        'title': 'Multi-Threading Design Patterns',
        'description': 'Design patterns provide proven solutions to common multi-threading challenges. These patterns help structure concurrent code to be correct, efficient, and maintainable.',
        'content': [
            {
                'subtitle': 'Producer-Consumer Pattern',
                'text': 'One or more producer threads generate data and place it in a shared buffer, while consumer threads take data from the buffer and process it. A bounded buffer (fixed-size queue) with proper synchronization prevents overflow and underflow. In Python, queue.Queue is a thread-safe implementation of this pattern. This pattern decouples data production from consumption.'
            },
            {
                'subtitle': 'Thread Pool Pattern',
                'text': 'Instead of creating a new thread for each task, a fixed pool of worker threads is created upfront. Tasks are submitted to a queue and the next available worker picks up a task. This avoids the overhead of thread creation/destruction and limits resource usage. In Python: concurrent.futures.ThreadPoolExecutor. Web servers like Apache use thread pools to handle HTTP requests.'
            },
            {
                'subtitle': 'Reader-Writer Pattern',
                'text': 'This pattern optimizes access when reads are far more frequent than writes. Multiple readers can access data simultaneously, but a writer needs exclusive access. Variations include reader-preference (readers never wait if no writer is active) and writer-preference (new readers wait if a writer is waiting). Used in database systems and caching layers.'
            },
            {
                'subtitle': 'Fork-Join Pattern',
                'text': 'A task is split (forked) into smaller subtasks that execute in parallel. Once all subtasks complete, their results are combined (joined). This is the foundation of divide-and-conquer parallelism. Example: parallel merge sort forks the array into halves, sorts each in a separate thread, then joins the results. Java ForkJoinPool and Python concurrent.futures implement this pattern.'
            },
        ],
        'key_concepts': ['Producer-Consumer', 'Thread Pool', 'Reader-Writer', 'Fork-Join', 'Bounded Buffer', 'Worker Threads'],
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
    .board-selector a { display: inline-block; padding: 8px 16px; margin: 5px; background: #2196F3; color: white; text-decoration: none; border-radius: 4px; }
    .board-selector a:hover { background: #1976D2; }
    .info { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
    pre { background: #f0f0f0; padding: 15px; border-radius: 5px; overflow-x: auto; }
    table.analysis { border-collapse: collapse; width: 100%; margin: 10px 0; }
    table.analysis td { border: 1px solid #ddd; padding: 8px; }
    .box-diagram td { border: 1px solid #333; width: 120px; height: 60px; text-align: center; font-size: 14px; }
</style>
"""


def app1(request):
    """Application 1: Sudoku Validator."""
    board_type = request.GET.get('board', 'valid')
    if board_type not in EXAMPLE_BOARDS:
        board_type = 'valid'

    current_board = EXAMPLE_BOARDS[board_type]
    is_valid, message = is_valid_sudoku(current_board)

    # Build board HTML table
    board_rows = ""
    for row in current_board:
        cells = ""
        for cell in row:
            css_class = ' class="empty"' if cell == '.' else ''
            cells += f"<td{css_class}>{cell}</td>"
        board_rows += f"<tr>{cells}</tr>"

    # Build board selector links
    board_links = ""
    for b in EXAMPLE_BOARDS.keys():
        label = b.replace("_", " ").title()
        board_links += f'<a href="?board={b}">{label}</a> '

    # Validation result
    status_text = "VALID" if is_valid else "INVALID"
    result_class = "valid" if is_valid else "invalid"

    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sudoku Validator - Juan Pablo Sanchez</title>
            {SUDOKU_STYLE}
        </head>
        <body>
            <p><a href="/juan_pablo/">Back to Home</a></p>
            <h1>Sudoku Validator</h1>
            <p>LeetCode Problem #36 - Validate a 9x9 Sudoku board</p>

            <h3>Current Board: {board_type.replace('_', ' ').title()}</h3>
            <table class="board-table">
                {board_rows}
            </table>

            <div class="board-selector">
                <strong>Select a board:</strong><br>
                {board_links}
            </div>

            <h3>Validation Result</h3>
            <div class="{result_class}">
                <strong>{status_text}</strong>
                <p>{message}</p>
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
                <p>The algorithm validates the board in <strong>three separate passes</strong>, each checking one constraint using a hash set to detect duplicates:</p>

                <h3>Pass 1 &mdash; Validate Rows</h3>
                <p>For each of the 9 rows, iterate across all columns. A fresh set tracks the digits seen so far. If a digit is already in the set, the row contains a duplicate and the board is invalid.</p>
                <pre># Walk each row left-to-right
for i in range(9):
    seen = set()
    for j in range(9):
        item = board[i][j]
        if item in seen:
            return False      # duplicate in this row
        elif item != '.':
            seen.add(item)    # remember this digit</pre>

                <h3>Pass 2 &mdash; Validate Columns</h3>
                <p>Same logic, but the indices are swapped (<code>board[j][i]</code>) so we walk top-to-bottom down each column instead of left-to-right across a row.</p>
                <pre># Walk each column top-to-bottom (note swapped indices)
for i in range(9):
    seen = set()
    for j in range(9):
        item = board[j][i]    # j is row, i is column
        if item in seen:
            return False
        elif item != '.':
            seen.add(item)</pre>

                <h3>Pass 3 &mdash; Validate 3x3 Boxes</h3>
                <p>Each box is identified by the (row, col) of its top-left corner. We list all nine starting positions explicitly, then scan the 3&times;3 area from each start.</p>
                <pre># All nine top-left corners
box_starts = [(0,0), (0,3), (0,6),
              (3,0), (3,3), (3,6),
              (6,0), (6,3), (6,6)]

for start_row, start_col in box_starts:
    seen = set()
    for row in range(start_row, start_row + 3):
        for col in range(start_col, start_col + 3):
            item = board[row][col]
            if item in seen:
                return False
            elif item != '.':
                seen.add(item)</pre>
            </div>

            <div class="info">
                <h2>Complexity Analysis</h2>
                <table class="analysis">
                    <tr>
                        <td><strong>Time Complexity</strong></td>
                        <td><strong>O(n&sup2;)</strong> where n = 9. Three passes each scan all 81 cells, giving 3 &times; 81 = 243 operations &mdash; still constant for a fixed board size.</td>
                    </tr>
                    <tr>
                        <td><strong>Space Complexity</strong></td>
                        <td><strong>O(n)</strong> where n = 9. Only one set of at most 9 elements exists at a time (re-created for each row, column, or box).</td>
                    </tr>
                    <tr>
                        <td><strong>Data Structure</strong></td>
                        <td><strong>Hash Set</strong> &mdash; Provides O(1) average-case lookup, making duplicate detection efficient.</td>
                    </tr>
                </table>
            </div>

            <div class="info">
                <h2>Why Three Separate Passes?</h2>
                <p>Splitting the validation into three independent passes makes the code easier to read and reason about. Each pass has a single responsibility:</p>
                <ul>
                    <li><strong>Pass 1</strong> only cares about rows &mdash; the inner loop moves across columns.</li>
                    <li><strong>Pass 2</strong> only cares about columns &mdash; the indices are simply swapped.</li>
                    <li><strong>Pass 3</strong> only cares about boxes &mdash; the start positions are listed explicitly so there is no index math to decode.</li>
                </ul>
                <p>A single-pass approach (using 27 sets simultaneously) is also valid and equally efficient, but the three-pass version is more transparent for learning purposes.</p>
            </div>

            <div class="info">
                <h2>3x3 Box Layout</h2>
                <p>The board is divided into nine 3&times;3 sub-boxes. Each box is scanned starting from its top-left corner:</p>
                <table class="box-diagram">
                    <tr>
                        <td>Box (0,0)<br>rows 0-2, cols 0-2</td>
                        <td>Box (0,3)<br>rows 0-2, cols 3-5</td>
                        <td>Box (0,6)<br>rows 0-2, cols 6-8</td>
                    </tr>
                    <tr>
                        <td>Box (3,0)<br>rows 3-5, cols 0-2</td>
                        <td>Box (3,3)<br>rows 3-5, cols 3-5</td>
                        <td>Box (3,6)<br>rows 3-5, cols 6-8</td>
                    </tr>
                    <tr>
                        <td>Box (6,0)<br>rows 6-8, cols 0-2</td>
                        <td>Box (6,3)<br>rows 6-8, cols 3-5</td>
                        <td>Box (6,6)<br>rows 6-8, cols 6-8</td>
                    </tr>
                </table>
            </div>

            <div class="info">
                <h2>Complete Solution</h2>
                <pre>class Solution:
    def isValidSudoku(self, board: List[List[str]]) -&gt; bool:
        # Validate Rows
        for i in range(9):
            s = set()
            for j in range(9):
                item = board[i][j]
                if item in s:
                    return False
                elif item != '.':
                    s.add(item)

        # Validate Cols
        for i in range(9):
            s = set()
            for j in range(9):
                item = board[j][i]
                if item in s:
                    return False
                elif item != '.':
                    s.add(item)

        # Validate Boxes
        starts = [(0, 0), (0, 3), (0, 6),
                  (3, 0), (3, 3), (3, 6),
                  (6, 0), (6, 3), (6, 6)]

        for i, j in starts:
            s = set()
            for row in range(i, i+3):
                for col in range(j, j+3):
                    item = board[row][col]
                    if item in s:
                        return False
                    elif item != '.':
                        s.add(item)
        return True

# Time Complexity: O(n^2)
# Space Complexity: O(n)</pre>
            </div>
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
    """Application 2: Multi-Threaded Programming."""
    # Build table of contents
    toc_html = ""
    for topic_id, topic in MULTITHREADING_DATA.items():
        toc_html += f'<a href="#{topic_id}">{topic["title"]}</a> '

    # Build all topic sections
    topics_html = ""
    for topic_id, topic in MULTITHREADING_DATA.items():
        # Key concepts as badges
        concepts = ""
        for c in topic['key_concepts']:
            concepts += f"<span>{c}</span> "

        # Content sub-sections
        content_html = ""
        for section in topic['content']:
            content_html += f"""
                <div class="subsection">
                    <h4>{section['subtitle']}</h4>
                    <p>{section['text']}</p>
                </div>
            """

        topics_html += f"""
            <div class="topic" id="{topic_id}">
                <h2>{topic['title']}</h2>
                <p>{topic['description']}</p>
                <div class="key-concepts">
                    <strong>Key Concepts:</strong><br>
                    {concepts}
                </div>
                {content_html}
            </div>
        """

    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Multi-Threaded Programming - Juan Pablo Sanchez</title>
            {THREADING_STYLE}
        </head>
        <body>
            <p><a href="/juan_pablo/">Back to Home</a></p>
            <h1>Multi-Threaded Programming</h1>
            <p>Understanding concurrency, synchronization, and parallel execution in software</p>

            <div class="toc">
                <strong>Topics:</strong><br>
                {toc_html}
            </div>

            {topics_html}
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
    """Application 3: Graphene Presentation."""
    sorted_sections = sorted(GRAPHENE_DATA.items(), key=lambda x: x[1]['order'])

    # Build table of contents
    toc_html = ""
    for section_id, section in sorted_sections:
        toc_html += f'<a href="#{section_id}">{section["order"]}. {section["title"]}</a> '

    # Build all sections
    sections_html = ""
    for section_id, section in sorted_sections:
        # Main content paragraphs
        content_paragraphs = ""
        for para in section['content'].split('\n\n'):
            if para.strip():
                content_paragraphs += f"<p>{para.strip()}</p>"

        # Section-specific extra content
        extra_html = ""

        # Key properties (what-is section)
        if 'key_properties' in section:
            props = ""
            for p in section['key_properties']:
                props += f"<li>{p}</li>"
            extra_html += f'<h3>Key Properties</h3><ul class="props">{props}</ul>'

        # Categories (applications section)
        if 'categories' in section:
            cats_html = ""
            for cat in section['categories']:
                items = ""
                for item in cat['items']:
                    items += f"<li>{item}</li>"
                cats_html += f'<div class="category"><h4>{cat["name"]}</h4><ul>{items}</ul></div>'
            extra_html += f"<h3>Applications by Category</h3>{cats_html}"

        # Types table (types section)
        if 'types_table' in section:
            rows = ""
            for t in section['types_table']:
                rows += f"<tr><td><strong>{t['name']}</strong></td><td>{t['price']}</td><td>{t['use_cases']}</td></tr>"
            extra_html += f"""
                <h3>Types and Pricing</h3>
                <table>
                    <thead><tr><th>Type</th><th>Price Range</th><th>Use Cases</th></tr></thead>
                    <tbody>{rows}</tbody>
                </table>
            """

        # Methods (production section)
        if 'methods' in section:
            methods_html = ""
            for m in section['methods']:
                methods_html += f"""
                    <div class="method">
                        <h4>{m['name']}</h4>
                        <p>{m['description']}</p>
                        <ul>
                            <li><strong>Quality:</strong> {m['quality']}</li>
                            <li><strong>Scalability:</strong> {m['scalability']}</li>
                            <li><strong>Setup Cost:</strong> {m['cost']}</li>
                            <li><strong>Output:</strong> {m['output']}</li>
                        </ul>
                    </div>
                """
            extra_html += f"<h3>Production Methods Comparison</h3>{methods_html}"

        # Barriers (adoption section)
        if 'barriers' in section:
            barriers_html = ""
            for b in section['barriers']:
                barriers_html += f'<div class="barrier"><h4>{b["title"]}</h4><p>{b["description"]}</p></div>'
            extra_html += f"<h3>Adoption Barriers</h3>{barriers_html}"

        # Why start now (adoption section)
        if 'why_start_now' in section:
            reasons = ""
            for r in section['why_start_now']:
                reasons += f"<li>{r}</li>"
            extra_html += f"<h3>Why Start Now?</h3><ul>{reasons}</ul>"

        sections_html += f"""
            <div class="section" id="{section_id}">
                <h2>{section['order']}. {section['title']}</h2>
                {content_paragraphs}
                {extra_html}
            </div>
        """

    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Graphene Presentation - Juan Pablo Sanchez</title>
            {GRAPHENE_STYLE}
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

            <div class="toc">
                <strong>Sections:</strong><br>
                {toc_html}
            </div>

            {sections_html}
        </body>
        </html>
    """
    return HttpResponse(html)
