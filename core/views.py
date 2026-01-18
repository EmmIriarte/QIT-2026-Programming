from django.http import HttpResponse

# List of all students with their display names and URL paths
STUDENTS = [
    {'name': 'Juan Pablo', 'path': 'juan_pablo'},
    {'name': 'Cesar', 'path': 'cesar'},
    {'name': 'Atheer', 'path': 'atheer'},
    {'name': 'Emmanuel', 'path': 'emmanuel'},
    {'name': 'Praneet', 'path': 'praneet'},
    {'name': 'Frankie', 'path': 'frankie'},
]


def global_index(request):
    """Global index page that displays a list of all students."""
    links_html = '\n'.join([
        f'        <li><a href="/{student["path"]}/">{student["name"]}</a></li>'
        for student in STUDENTS
    ])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>QIT 2026 Programming - Student Index</title>
</head>
<body>
    <h1>QIT 2026 Programming - Student Index</h1>
    <ul>
{links_html}
    </ul>
</body>
</html>"""
    
    return HttpResponse(html)
