from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import datetime


def index(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Atheer's Section</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }
            h1 { color: #6a1b9a; }
            a { color: #6a1b9a; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px; }
            .card h2 { margin-top: 0; }
            .back { margin-bottom: 20px; display: inline-block; }
        </style>
    </head>
    <body>
        <a class="back" href="/">&larr; Home</a>
        <h1>Atheer's Section</h1>
        <div class="card">
            <h2><a href="/atheer/app1/">App 1 - LeetCode: Longest Substring</a></h2>
            <p>Sliding window solution for LeetCode #3.</p>
        </div>
        <div class="card">
            <h2><a href="/atheer/app2/">App 2 - Schrodinger's Cat</a></h2>
            <p>Quantum mechanics simulation of Schrodinger's cat thought experiment.</p>
        </div>
        <div class="card">
            <h2><a href="/atheer/app3/">App 3 - Todo List</a></h2>
            <p>Task management application overview.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def app1_leetcode(request):
    from .leetcode import Solution
    sol = Solution()

    test_cases = [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        ("dvdf", 3),
        ("anviaj", 5),
    ]

    rows = ""
    for s, expected in test_cases:
        result = sol.lengthOfLongestSubstring(s)
        status = "Pass" if result == expected else "Fail"
        color = "#4caf50" if status == "Pass" else "#f44336"
        display = f'"{s}"' if s else '""'
        rows += f'<tr><td>{display}</td><td>{expected}</td><td>{result}</td><td style="color:{color};font-weight:bold;">{status}</td></tr>'

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>LeetCode #3 - Longest Substring</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }}
            h1 {{ color: #6a1b9a; }}
            h2 {{ color: #7b1fa2; }}
            .card {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            a {{ color: #6a1b9a; }}
            table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #f3e5f5; color: #6a1b9a; }}
            pre {{ background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <a href="/atheer/">&larr; Back to Atheer's Section</a>

        <div class="card">
            <h1>LeetCode #3: Longest Substring Without Repeating Characters</h1>
            <p><strong>Difficulty:</strong> Medium</p>
            <p>Given a string <code>s</code>, find the length of the longest substring
            without repeating characters.</p>
        </div>

        <div class="card">
            <h2>Solution (Sliding Window)</h2>
            <pre>
class Solution:
    def lengthOfLongestSubstring(self, s: str) -&gt; int:
        char_dict = {{}}
        max_len = 0
        start = 0

        for end in range(len(s)):
            if s[end] in char_dict:
                start = max(start, char_dict[s[end]] + 1)
            char_dict[s[end]] = end
            max_len = max(max_len, end - start + 1)

        return max_len</pre>
            <p><strong>Time Complexity:</strong> O(n) &mdash; single pass through the string.</p>
            <p><strong>Space Complexity:</strong> O(min(m, n)) &mdash; where m is the character set size.</p>
        </div>

        <div class="card">
            <h2>Test Results</h2>
            <table>
                <tr><th>Input</th><th>Expected</th><th>Result</th><th>Status</th></tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def app2_schrodinger(request):
    """Schrodinger's Cat Simulator - matches Atheer's original catbox app."""
    # Default: superposition (box not yet opened)
    cat_state = "superposition"
    if 'observe' in request.GET:
        cat_state = random.choice(["alive", "dead"])

    image_file = f"{cat_state}_cat.png"

    if cat_state == "alive":
        color = "#4caf50"
        label = "ALIVE"
        desc = "The cat is alive! The atom did not decay."
    elif cat_state == "dead":
        color = "#f44336"
        label = "DEAD"
        desc = "The cat is dead. The atom decayed and triggered the mechanism."
    else:
        color = "#ff9800"
        label = "SUPERPOSITION"
        desc = "The box is sealed. The cat is simultaneously alive and dead until observed."

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Schrodinger's Cat Simulator</title>
        <style>
            body {{ text-align: center; font-family: Arial, sans-serif; margin-top: 30px; background: #f0f0f0; }}
            h1 {{ color: #333; }}
            img {{ border: 3px solid #333; border-radius: 10px; margin-top: 20px; }}
            .observe-btn {{
                margin-top: 20px; padding: 10px 20px; font-size: 16px;
                cursor: pointer; border: none; border-radius: 5px;
                background-color: #ff6666; color: white; display: inline-block;
                text-decoration: none;
            }}
            .observe-btn:hover {{ background-color: #ff4d4d; }}
            .result-label {{ font-size: 28px; font-weight: bold; margin-top: 15px; color: {color}; }}
            .desc {{ font-size: 16px; color: #555; margin-top: 10px; max-width: 500px; margin-left: auto; margin-right: auto; }}
            .back {{ display: inline-block; margin-bottom: 15px; color: #6a1b9a; text-decoration: none; }}
            .back:hover {{ text-decoration: underline; }}
            .theory {{ max-width: 600px; margin: 30px auto; background: white; padding: 20px; border-radius: 8px;
                       box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: left; }}
            .theory h2 {{ color: #333; }}
        </style>
    </head>
    <body>
        <a class="back" href="/atheer/">&larr; Back to Atheer's Section</a>
        <h1>Schrodinger's Cat Simulator</h1>

        <img src="/static/atheer/{image_file}" width="300" alt="{cat_state} cat" />

        <div class="result-label">{label}</div>
        <p class="desc">{desc}</p>

        <form method="get">
            <button class="observe-btn" name="observe" type="submit">Observe the Cat</button>
        </form>

        <div class="theory">
            <h2>The Thought Experiment</h2>
            <p>Proposed by Erwin Schrodinger in 1935, this thought experiment illustrates
            the apparent paradox of applying quantum superposition to everyday objects.
            A cat is placed in a sealed box with a radioactive atom, a Geiger counter,
            and a vial of poison. If the atom decays, the poison kills the cat.</p>
            <p>According to the Copenhagen interpretation of quantum mechanics, until the box
            is opened and the cat observed, it exists in a superposition of both alive and dead
            states simultaneously.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def _get_tasks(request):
    """Get tasks list from session storage."""
    if 'atheer_tasks' not in request.session:
        request.session['atheer_tasks'] = []
    return request.session['atheer_tasks']


def _save_tasks(request, tasks):
    """Save tasks list to session storage."""
    request.session['atheer_tasks'] = tasks
    request.session.modified = True


# CSS matching Atheer's original style.css from her todo-List project
TODO_CSS = """
* { box-sizing: border-box; font-family: "Segoe UI", Helvetica, Arial, sans-serif; }
body { background: #f0f2f5; margin: 0; padding: 20px; }
.container { max-width: 600px; margin: 30px auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.15); }
h1 { text-align: center; color: #1877f2; font-size: 26px; margin-bottom: 20px; }
input[type="text"], input[type="password"], textarea {
    width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #ddd;
    margin-bottom: 12px; font-size: 14px;
}
input:focus, textarea:focus { outline: none; border-color: #1877f2; box-shadow: 0 0 0 1px #1877f2; }
input[type="submit"], .btn {
    display: inline-block; background: #1877f2; color: white; border: none;
    padding: 12px 20px; border-radius: 6px; font-size: 16px; font-weight: bold;
    cursor: pointer; text-decoration: none; text-align: center;
}
input[type="submit"]:hover, .btn:hover { background: #166fe5; }
.btn-danger { background: #dc3545; }
.btn-danger:hover { background: #c82333; }
.btn-sm { padding: 6px 12px; font-size: 13px; font-weight: normal; }
a { color: #1877f2; text-decoration: none; font-weight: 500; }
a:hover { text-decoration: underline; }
table { width: 100%; border-collapse: collapse; text-align: center; margin: 15px 0; }
th, td { padding: 12px 10px; border-bottom: 1px solid #ddd; }
th { background: #f0f2f5; color: #1877f2; }
tr:hover { background: #f1f1f1; }
.complete { text-decoration: line-through; color: #999; }
.search-row { display: flex; gap: 8px; margin-bottom: 15px; }
.search-row input[type="text"] { margin-bottom: 0; flex: 1; }
.search-row input[type="submit"] { width: auto; }
.count { text-align: center; color: #666; margin-bottom: 15px; }
.back-link { display: inline-block; margin-bottom: 15px; }
.add-row { text-align: center; margin-bottom: 15px; }
"""


def app3_todo(request):
    """My To Do List - task list view with search."""
    tasks = _get_tasks(request)

    search = request.GET.get('search-area', '')
    filtered = tasks
    if search:
        filtered = [t for t in tasks if search.lower() in t['title'].lower()]

    incomplete_count = sum(1 for t in tasks if not t['complete'])

    rows = ""
    if filtered:
        for task in filtered:
            tid = task['id']
            title_class = 'class="complete"' if task['complete'] else ''
            status_icon = "&#10003;" if task['complete'] else "&#9675;"
            rows += f"""<tr>
                <td {title_class}>{task['title']}</td>
                <td><a href="/atheer/app3/toggle/{tid}/">{status_icon}</a></td>
                <td><a href="/atheer/app3/delete/{tid}/" class="btn btn-danger btn-sm">Delete</a></td>
            </tr>"""
    else:
        rows = '<tr><td colspan="3"><em>No items</em></td></tr>'

    search_val = f'value="{search}"' if search else ''

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My To Do List</title>
        <style>{TODO_CSS}</style>
    </head>
    <body>
        <div class="container">
            <a class="back-link" href="/atheer/">&larr; Back to Atheer's Section</a>
            <h1>My To Do List</h1>
            <p class="count">{incomplete_count} task(s) remaining</p>

            <div class="add-row">
                <a class="btn" href="/atheer/app3/create/">Add Task</a>
            </div>

            <form method="GET" class="search-row">
                <input type="text" name="search-area" placeholder="Search tasks..." {search_val}>
                <input type="submit" value="Search">
            </form>

            <table>
                <tr>
                    <th>Item</th>
                    <th>Status</th>
                    <th></th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


@csrf_exempt
def app3_todo_create(request):
    """Create a new task."""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title:
            tasks = _get_tasks(request)
            new_id = max((t['id'] for t in tasks), default=0) + 1
            tasks.append({
                'id': new_id,
                'title': title,
                'description': description,
                'complete': False,
                'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
            })
            _save_tasks(request, tasks)
        return HttpResponseRedirect('/atheer/app3/')

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Task</title>
        <style>{TODO_CSS}</style>
    </head>
    <body>
        <div class="container">
            <a class="back-link" href="/atheer/app3/">&larr; Back to list</a>
            <h1>Add Task</h1>
            <form method="POST">
                <label style="font-weight:bold;display:block;margin-bottom:5px;">Title:</label>
                <input type="text" name="title" required placeholder="Enter task title">
                <label style="font-weight:bold;display:block;margin-bottom:5px;">Description (optional):</label>
                <textarea name="description" rows="3" placeholder="Enter description"></textarea>
                <input type="submit" value="Submit">
            </form>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def app3_todo_toggle(request, task_id):
    """Toggle task complete/incomplete."""
    tasks = _get_tasks(request)
    for task in tasks:
        if task['id'] == task_id:
            task['complete'] = not task['complete']
            break
    _save_tasks(request, tasks)
    return HttpResponseRedirect('/atheer/app3/')


def app3_todo_delete(request, task_id):
    """Delete a task."""
    tasks = _get_tasks(request)
    tasks = [t for t in tasks if t['id'] != task_id]
    _save_tasks(request, tasks)
    return HttpResponseRedirect('/atheer/app3/')
