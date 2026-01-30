from django.http import HttpResponse

def index(request):
    html = """
    <h1>Cesar's Section</h1>
    <ul>
        <li><a href="/cesar/app1/">App 1 - Schmidt Rank</a></li>
        <li><a href="/cesar/app2/">App 2 - Study Planner</a></li>
        <li><a href="/cesar/app3/">App 3 - LeetCode</a></li>
    </ul>
    """
    return HttpResponse(html)
