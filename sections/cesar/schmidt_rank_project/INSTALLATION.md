# Schmidt Rank Calculator - Installation Guide

Step-by-step installation guide for Windows 11 with PyCharm.

## Quick Start

```bash
# 1. Extract project
# 2. Open in PyCharm
# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Run server
python manage.py runserver

# 8. Open browser
# http://127.0.0.1:8000/
```

## Detailed Instructions

### Step 1: Prerequisites

- Python 3.11+ ✅
- PyCharm ✅
- pip ✅

### Step 2: Extract Project

Extract `schmidt_rank_project` to your desired location, e.g.:
```
C:\Users\YourName\Documents\schmidt_rank_project
```

### Step 3: Open in PyCharm

1. Open PyCharm
2. File → Open
3. Select `schmidt_rank_project` folder

### Step 4: Create Virtual Environment

PyCharm will ask to create venv. Click OK, or:

Terminal in PyCharm:
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 5.0
- NumPy (for calculations)
- SciPy (for SVD)
- Matplotlib (for plots)
- Bootstrap forms

### Step 6: Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Admin Account (Optional)

```bash
python manage.py createsuperuser
```

Enter username and password when prompted.

### Step 8: Run Server

```bash
python manage.py runserver
```

### Step 9: Access Application

- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Usage Examples

### Example 1: Bell State

1. Go to home page
2. Select "Predefined State"
3. Choose "Bell State |Φ+⟩"
4. Click "Calculate"
5. Result: Schmidt rank = 2 (maximally entangled)

### Example 2: Product State

1. Select "Manual Input"
2. Enter: `1, 0, 0, 0`
3. Dimensions: 2 × 2
4. Click "Calculate"
5. Result: Schmidt rank = 1 (not entangled)

### Example 3: Random State

1. Select "Random State"
2. Dimensions: 2 × 2
3. Target rank: 2
4. Click "Calculate"
5. Result: Random entangled state

## Troubleshooting

### NumPy/SciPy Installation Issues

If you get errors with NumPy or SciPy:

```bash
pip install numpy==1.26.3
pip install scipy==1.11.4
```

### Migration Issues

```bash
python manage.py makemigrations calculator
python manage.py migrate
```

### Server Won't Start

Check if port 8000 is free:
```bash
netstat -ano | findstr :8000
```

Use different port:
```bash
python manage.py runserver 8080
```

## Project Structure

```
schmidt_rank_project/
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── calculator/
    ├── models.py          # Database models
    ├── views.py           # View logic
    ├── schmidt.py         # Calculations
    ├── forms.py           # Input forms
    ├── admin.py           # Admin panel
    ├── templates/         # HTML templates
    └── migrations/        # Database migrations
```

## Adding to GitHub

See main `study_planner` project's `GITHUB_SETUP.md` for detailed instructions.

Quick version:
```bash
cd schmidt_rank_project
git init
git add .
git commit -m "Initial commit - Schmidt Rank Calculator"
git remote add origin YOUR_REPO_URL
git push -u origin main
```

## Features

✅ Calculate Schmidt rank
✅ Schmidt decomposition
✅ Predefined quantum states
✅ Random state generation
✅ Visualization with Chart.js
✅ Calculation history
✅ Admin panel
✅ Von Neumann entropy

## Next Steps

1. Test with different quantum states
2. Add more predefined states
3. Implement export to PDF
4. Add API endpoints
5. Create visualization improvements

## References

- Nielsen & Chuang, "Quantum Computation and Quantum Information"
- QIT Course, University of Gdańsk

## Support

For issues, check:
1. Python version (3.11+)
2. All dependencies installed
3. Migrations run
4. Server running on correct port

Happy calculating! 🎉
