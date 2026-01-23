# Django Fundamentals Guide

A comprehensive guide to understanding Django project structure, routing, and core concepts based on a practical implementation.

---

## 1. Django Project Structure

Here's the complete project structure I created:

```
QIT-2026-Programming/            ← Project root
├── venv/                        ← Virtual environment (isolated Python)
├── manage.py                    ← Command-line tool for Django
├── core/                        ← Project configuration folder
│   ├── __init__.py
│   ├── settings.py              ← Main settings (apps, database, etc.)
│   ├── urls.py                  ← Main URL router
│   ├── wsgi.py                  ← Web server gateway
│   └── asgi.py                  ← Async server gateway
└── sections/                    ← Main Django app
    ├── __init__.py
    ├── README.md                ← This file
    ├── prabhneet/               ← Namespace/module folder
    │   ├── __init__.py
    │   ├── views.py             ← Home view
    │   ├── urls.py              ← Main router, includes app1 and app2 URLs
    │   ├── app1/                ← Sub-module for triangular sum
    │   │   ├── __init__.py
    │   │   ├── views.py         ← triangular_sum view
    │   │   └── urls.py          ← triangular_sum URL
    │   └── app2/                ← Sub-module for Bloch sphere
    │       ├── __init__.py
    │       ├── views.py         ← bloch view
    │       └── urls.py          ← bloch URL
    ├── templates/
    │   ├── home.html            ← Homepage template
    │   ├── triangular_sum.html  ← Triangular sum template
    │   └── bloch.html           ← Bloch sphere template
    └── static/
        └── prabhneet/
            └── app1/
                └── images/
                    └── triangular_sum_diagram.png
```

---

## 2. Key Concepts

### Project vs App

- **Project** (`core/`) = The entire website configuration
- **App** (`sections/`) = Main Django application
- **Modules** (`prabhneet/`, `prabhneet/app1/`, `prabhneet/app2/`) = Feature-specific modules within the app

**Analogy:**
- **Project** = The building foundation
- **App** = The main building (sections)
- **Modules** = Different rooms/departments within the building

This structure allows for organized, modular code where each feature has its own dedicated space.

---

## 3. The Request-Response Flow

Here's what happens when you visit `http://127.0.0.1:8000/prabhneet/app1/triangular-sum/`:

```
1. Browser sends request
   ↓
2. Django receives it at manage.py runserver
   ↓
3. Goes to core/urls.py (main router)
   ↓
4. Matches pattern: path('prabhneet/', include('sections.prabhneet.urls'))
   ↓
5. Goes to sections/prabhneet/urls.py
   ↓
6. Matches pattern: path('app1/', include('sections.prabhneet.app1.urls'))
   ↓
7. Goes to sections/prabhneet/app1/urls.py
   ↓
8. Matches pattern: path('triangular-sum/', views.triangular_sum)
   ↓
9. Calls the view function in sections/prabhneet/app1/views.py
   ↓
10. View processes request and renders template
   ↓
11. Returns HTML response to browser
   ↓
12. Browser displays the page
```

---

## 4. URL Routing (The Phone Directory)

### Main Router (`core/urls.py`)

```python
urlpatterns = [
    path('admin/', admin.site.urls),                      # Django admin panel
    path('prabhneet/', include('sections.prabhneet.urls')), # Main module
]
```

**How it works:**
- `path('admin/', ...)` → Matches `http://127.0.0.1:8000/admin/`
- `path('prabhneet/', ...)` → Matches `http://127.0.0.1:8000/prabhneet/...`
- `include()` → Delegates to the module's urls.py

### Module Router (`sections/prabhneet/urls.py`)

```python
from django.urls import path, include
from . import views

app_name = 'prabhneet'

urlpatterns = [
    path('', views.home, name='home'),
    path('app1/', include('sections.prabhneet.app1.urls')),
    path('app2/', include('sections.prabhneet.app2.urls')),
]
```

### Sub-module Router (`sections/prabhneet/app1/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'app1'

urlpatterns = [
    path('triangular-sum/', views.triangular_sum, name='triangular_sum'),
]
```

### Sub-module Router (`sections/prabhneet/app2/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'app2'

urlpatterns = [
    path('bloch/', views.bloch, name='bloch'),
]
```

**Full URLs become:**
- **App1:** `http://127.0.0.1:8000/prabhneet/app1/triangular-sum/`
- **App2:** `http://127.0.0.1:8000/prabhneet/app2/bloch/`

**The `name` parameter:**
- Allows you to reference URLs by name instead of hardcoding
- In templates: 
  - `{% url 'prabhneet:app1:triangular_sum' %}`
  - `{% url 'prabhneet:app2:bloch' %}`
- Much better than hardcoding `/prabhneet/app1/triangular-sum/`

---

## 5. Views (The Brain)

Views are Python functions that handle requests and return responses.

### Simple View (`sections/prabhneet/views.py`)

```python
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
```

**What happens:**
1. Takes a `request` object (contains info about the HTTP request)
2. `render()` combines a template with data
3. Returns an HTML response

### View with Context (passing data to template)

```python
def home(request):
    context = {
        'title': 'Prabhneet Singh - Programming Lab Exam',
        'apps': ['Triangular Sum', 'Bloch Sphere']
    }
    return render(request, 'home.html', context)
```

In the template, you can use:

```html
<h1>{{ title }}</h1>
{% for app in apps %}
    <p>{{ app }}</p>
{% endfor %}
```

---

## 6. Templates (The Face)

Templates are HTML files with Django template language.

### Template Location

Django looks for templates in:
1. `sections/templates/` folder (our structure)

**Our structure:**
- `sections/templates/home.html` - Homepage
- `sections/templates/triangular_sum.html` - Triangular sum page
- `sections/templates/bloch.html` - Bloch sphere page

**Simple flat structure:**
- All templates are directly in the `templates/` folder
- No nested folders needed for this project
- Easy to locate and reference

### Static Files Location

Static files (CSS, JavaScript, images) are stored in:
- `sections/static/prabhneet/` folder

**Example:**
- Image: `sections/static/prabhneet/app1/images/triangular_sum_diagram.png`

**In templates, reference as:**
```html
{% load static %}
<img src="{% static 'prabhneet/app1/images/triangular_sum_diagram.png' %}" alt="Diagram">
```

### Template Tags

```html
<!-- Variables -->
{{ variable_name }}

<!-- URL linking -->
<a href="{% url 'prabhneet:app1:triangular_sum' %}">Triangular Sum</a>
<a href="{% url 'prabhneet:app2:bloch' %}">Bloch Sphere</a>

<!-- Conditionals -->
{% if user.is_authenticated %}
    <p>Welcome!</p>
{% endif %}

<!-- Loops -->
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}

<!-- Load static files -->
{% load static %}
<img src="{% static 'prabhneet/app1/images/triangular_sum_diagram.png' %}">
```

---

## 7. Settings.py (The Control Center)

### INSTALLED_APPS

```python
INSTALLED_APPS = [
    'django.contrib.admin',      # Built-in: Admin panel
    'django.contrib.auth',       # Built-in: User authentication
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Built-in: Static files (CSS, JS, images)
    'sections',                   # Your main app
]
```

**You must register every app here** or Django won't recognize it!

### STATIC_URL

```python
STATIC_URL = '/static/'
```

---

## 8. How Our Apps Work Together

### Homepage Flow

```
User visits: http://127.0.0.1:8000/prabhneet/
    ↓
core/urls.py: path('prabhneet/', include('sections.prabhneet.urls'))
    ↓
sections/prabhneet/urls.py: path('', views.home, name='home')
    ↓
sections/prabhneet/views.py: def home(request)
    ↓
Renders: sections/templates/home.html
    ↓
User sees: Homepage with links to app1 and app2
```

### Clicking on Triangular Sum

```
User clicks: {% url 'prabhneet:app1:triangular_sum' %}
    ↓
Resolves to: /prabhneet/app1/triangular-sum/
    ↓
core/urls.py: path('prabhneet/', include('sections.prabhneet.urls'))
    ↓
sections/prabhneet/urls.py: path('app1/', include('sections.prabhneet.app1.urls'))
    ↓
sections/prabhneet/app1/urls.py: path('triangular-sum/', views.triangular_sum)
    ↓
sections/prabhneet/app1/views.py: def triangular_sum(request)
    ↓
Renders: sections/templates/triangular_sum.html
```

### Clicking on Bloch Sphere

```
User clicks: {% url 'prabhneet:app2:bloch' %}
    ↓
Resolves to: /prabhneet/app2/bloch/
    ↓
core/urls.py: path('prabhneet/', include('sections.prabhneet.urls'))
    ↓
sections/prabhneet/urls.py: path('app2/', include('sections.prabhneet.app2.urls'))
    ↓
sections/prabhneet/app2/urls.py: path('bloch/', views.bloch)
    ↓
sections/prabhneet/app2/views.py: def bloch(request)
    ↓
Renders: sections/templates/bloch.html
```

---

## 9. Namespace Pattern

Notice we used:
- `app_name = 'prabhneet'` in `sections/prabhneet/urls.py`
- `app_name = 'app1'` in `sections/prabhneet/app1/urls.py`
- `app_name = 'app2'` in `sections/prabhneet/app2/urls.py`
- `{% url 'prabhneet:app1:triangular_sum' %}` in templates (nested namespaces)
- `{% url 'prabhneet:app2:bloch' %}` in templates

**Why?**
- Nested namespaces allow clear organization: `prabhneet:app1:triangular_sum` and `prabhneet:app2:bloch`
- Multiple modules might have similarly named views
- Namespaces prevent conflicts and make URLs self-documenting

---

## 10. Django MVT Pattern

Django follows **MVT** (Model-View-Template):

```
┌─────────┐
│  Model  │  ← Database (we didn't use this yet)
└────┬────┘
     │
┌────▼────┐
│  View   │  ← Business logic (views.py)
└────┬────┘
     │
┌────▼────────┐
│  Template   │  ← Presentation (HTML files)
└─────────────┘
```

**What we built:**
- **Views:** `views.py` files (business logic)
- **Templates:** HTML files (what users see)
- **Models:** Not used yet (would handle database)

---

## 11. Common Django Commands

```bash
# Create new app
python manage.py startapp app_name

# Run development server
python manage.py runserver

# Check for errors
python manage.py check

# Create database tables (when using models)
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

---

## 12. File Responsibilities Summary

| File | Purpose | Example |
|------|---------|---------|
| `settings.py` | Project configuration | Register apps, set database, static files |
| `core/urls.py` | Main URL router | Route to different modules |
| `sections/prabhneet/urls.py` | Module URLs | Define module's URL patterns |
| `sections/prabhneet/app1/urls.py` | Sub-module URLs | Define feature-specific URLs |
| `sections/prabhneet/app2/urls.py` | Sub-module URLs | Define feature-specific URLs |
| `views.py` | Business logic | Handle requests, return responses |
| `templates/` | HTML files | What users see (flat structure) |
| `static/prabhneet/` | Static files | CSS, JS, images |
| `models.py` | Database structure | Define data (not used yet) |

---

## 13. Project Flow Diagram

```
┌──────────────────────────────────────────────────────┐
│                   User's Browser                      │
│         http://127.0.0.1:8000/prabhneet/              │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│              core/urls.py (Router)                    │
│  ┌───────────────────────────────────────────────┐  │
│  │ path('prabhneet/',                            │  │
│  │      include('sections.prabhneet.urls'))      │  │
│  └───────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────┘
                         │
                    ┌────▼────────────┐
                    │  sections/      │
                    │  prabhneet/     │
                    │  urls.py        │
                    └────┬──────┬─────┬────┘
                         │      │     │
                    ┌────▼──┐ ┌▼─────┐ ┌▼─────────┐
                    │views  │ │app1/ │ │app2/     │
                    │.py    │ │urls  │ │urls.py   │
                    └───┬───┘ └──┬───┘ └──┬───────┘
                        │        │        │
                   ┌────▼────┐ ┌▼───────┐ ┌▼────────┐
                   │home     │ │app1/   │ │app2/    │
                   │.html    │ │views.py│ │views.py │
                   └─────────┘ └──┬─────┘ └──┬──────┘
                                  │           │
                            ┌─────▼──────────┐ ┌──▼──────┐
                            │triangular_sum  │ │bloch    │
                            │.html           │ │.html    │
                            └────────────────┘ └─────────┘
                            
Templates (flat structure):
sections/templates/home.html
sections/templates/triangular_sum.html
sections/templates/bloch.html

Static Files:
sections/static/prabhneet/app1/images/triangular_sum_diagram.png
```

---

## 14. Key Takeaways

1. **Apps are modular** - Each app contains organized modules and features
2. **URL routing is hierarchical** - Main URLs → Module URLs → Sub-module URLs → Views
3. **Views connect everything** - They're the glue between URLs and templates
4. **Templates use special syntax** - `{{ }}` for variables, `{% %}` for logic
5. **Always register apps** - in `INSTALLED_APPS`
6. **Use URL names** - Never hardcode URLs, use `{% url 'namespace:name' %}`
7. **Organize by feature** - Group related code (views, templates, static files) by module
8. **Nested namespaces** - Use for complex apps: `prabhneet:app1:triangular_sum`

---

## Getting Started

1. **Clone the repository** (or create a new Django project)
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. **Install Django:**
   ```bash
   pip install django
   ```
5. **Navigate to project directory:**
   ```bash
   cd QIT-2026-Programming
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Visit:** `http://127.0.0.1:8000/prabhneet/`

---

## Project Components

### Main Module: Prabhneet
- **Base URL:** `/prabhneet/`
- **Description:** Main module containing student work
- **Homepage:** Interactive card-based navigation

### App 1: Triangular Sum Calculator
- **URL:** `/prabhneet/app1/triangular-sum/`
- **Description:** Calculate triangular sums with step-by-step visualization
- **LeetCode Problem:** #2221 (Medium)
- **Features:** 
  - Input validation
  - Visual step-by-step process
  - Time/Space complexity display (O(n²) time, O(1) space)
  - Diagram visualization
  - Interactive calculator

### App 2: Interactive Bloch Sphere
- **URL:** `/prabhneet/app2/bloch/`
- **Description:** Quantum state visualization on the Bloch sphere
- **Features:** 
  - Interactive sliders for theta (θ) and phi (φ) angles
  - Real-time quantum state formula updates
  - Preset buttons for common quantum states (|0⟩, |1⟩, |+⟩, |−⟩, |i⟩, |−i⟩)
  - Visual state vector representation
  - Educational information about quantum states

---

## Author

Prabhneet Singh  
Lecturer: Fernando Almaguer Angeles