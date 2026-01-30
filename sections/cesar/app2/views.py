from django.http import HttpResponse


def home(request):
    """Study Planner overview page."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Study Planner - Cesar</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }
            h1 { color: #2e7d32; }
            h2 { color: #388e3c; }
            .card { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .nav { margin-bottom: 20px; }
            .nav a { margin-right: 15px; color: #2e7d32; text-decoration: none; }
            .nav a:hover { text-decoration: underline; }
            .feature { background: #e8f5e9; border-left: 4px solid #4caf50; padding: 15px; margin: 10px 0; border-radius: 0 8px 8px 0; }
            table { width: 100%; border-collapse: collapse; margin: 15px 0; }
            th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #e8f5e9; color: #2e7d32; }
        </style>
    </head>
    <body>
        <div class="nav">
            <a href="/cesar/">&larr; Back to Cesar's Section</a>
        </div>

        <div class="card">
            <h1>Study Planner</h1>
            <p>A university study planning application designed to help students track their
            academic progress, manage courses, and monitor ECTS credits across programs.</p>
        </div>

        <div class="card">
            <h2>Features</h2>
            <div class="feature">
                <strong>Program Progress Tracking</strong>
                <p>Track ECTS credits earned across multiple academic programs with
                percentage-based progress visualization.</p>
            </div>
            <div class="feature">
                <strong>Course Management</strong>
                <p>View and filter courses by program, status (in progress, completed, failed),
                and semester type (winter/summer).</p>
            </div>
            <div class="feature">
                <strong>Assignment Tracking</strong>
                <p>Monitor upcoming and overdue assignments with deadline awareness.
                Filter by status and program.</p>
            </div>
            <div class="feature">
                <strong>Grade Statistics</strong>
                <p>Calculate GPA per program and overall. View grade distribution
                with detailed statistics.</p>
            </div>
        </div>

        <div class="card">
            <h2>Data Model</h2>
            <table>
                <tr><th>Model</th><th>Description</th><th>Key Fields</th></tr>
                <tr><td>Program</td><td>Academic degree program</td><td>name, total_ects_required</td></tr>
                <tr><td>Course</td><td>Individual course within a program</td><td>name, ects, semester_type</td></tr>
                <tr><td>Enrollment</td><td>Student's enrollment in a course</td><td>status, is_passed</td></tr>
                <tr><td>Assignment</td><td>Course assignment with deadline</td><td>title, due_date, is_completed</td></tr>
                <tr><td>Grade</td><td>Grade received for an enrollment</td><td>grade (float), date</td></tr>
            </table>
        </div>

        <div class="card">
            <h2>Technical Details</h2>
            <ul>
                <li>Built with Django's ORM for database management</li>
                <li>Uses Django's authentication system for user-specific data</li>
                <li>Implements filtering with Django's QuerySet API</li>
                <li>Calculates statistics using Django's aggregation functions (Avg, Sum, Count)</li>
                <li>Polish/European grading scale (2.0 - 5.0)</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
