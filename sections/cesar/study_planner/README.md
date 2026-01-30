# Study Planner

A Django-based web application for managing multiple university programs, courses, assignments, and grades.

## Features

- **Multi-Program Support**: Manage multiple master's programs simultaneously
- **Course Management**: Track courses across different programs and semesters
- **Assignment Tracking**: Keep track of deadlines, priorities, and completion status
- **Grade Management**: Record and calculate grades with automatic GPA calculation
- **Dashboard**: Unified view of all programs, upcoming deadlines, and progress
- **Statistics**: Visual charts and progress tracking

## Technology Stack

- **Backend**: Django 5.0+
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Charts**: Chart.js
- **Python**: 3.11+

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/study_planner.git
cd study_planner
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser** (admin account)
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Main app: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
study_planner/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
│
├── config/               # Main project configuration
│   ├── __init__.py
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   ├── asgi.py          # ASGI configuration
│   └── wsgi.py          # WSGI configuration
│
├── core/                 # Main application
│   ├── migrations/       # Database migrations
│   ├── templates/        # HTML templates
│   │   └── core/
│   ├── static/          # Static files (CSS, JS, images)
│   │   └── core/
│   ├── __init__.py
│   ├── admin.py         # Admin panel configuration
│   ├── apps.py          # App configuration
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL patterns
│   ├── forms.py         # Forms
│   └── tests.py         # Tests
│
└── db.sqlite3           # SQLite database (created after migrations)
```

## Database Models

### Program
Represents a university program (e.g., Quantum Information Technology)
- name, university, faculty, degree_type
- total_ects_required, is_active, color

### Course
Represents a course/subject
- program (FK), code, name, semester, year
- ects, course_type, description, instructor
- hours_per_week

### Enrollment
Student's enrollment in a course
- user (FK), course (FK), status
- enrolled_date, is_passed, notes

### Assignment
Tasks, projects, exams for courses
- course (FK), title, description, type
- due_date, priority, max_points
- is_completed, completed_date

### Grade
Grades for assignments or courses
- enrollment (FK), assignment (FK, optional)
- grade, points, max_points, weight
- date, comment

## Usage

### Adding a Program

1. Go to Admin Panel (http://127.0.0.1:8000/admin/)
2. Click on "Programs"
3. Click "Add Program"
4. Fill in the details:
   - Name: "Quantum Information Technology"
   - University: "University of Gdańsk"
   - Faculty: "Faculty of Mathematics, Physics and Informatics"
   - Degree Type: "Master's"
   - Total ECTS Required: 120
   - Color: Choose a color for the program
5. Save

### Adding Courses

1. In Admin Panel, go to "Courses"
2. Click "Add Course"
3. Select the program
4. Fill in course details (code, name, semester, ECTS, etc.)
5. Save

### Enrolling in Courses

1. In Admin Panel, go to "Enrollments"
2. Click "Add Enrollment"
3. Select your user and the course
4. Set status to "In Progress"
5. Save

## Development Roadmap

### Phase 1 (Current)
- [x] Basic project structure
- [x] Database models
- [x] Admin panel configuration
- [ ] Dashboard view
- [ ] Course list view
- [ ] Course detail view

### Phase 2
- [ ] Assignment management
- [ ] Grade tracking
- [ ] GPA calculation
- [ ] Calendar view

### Phase 3
- [ ] Statistics and charts
- [ ] Export functionality (PDF, Excel)
- [ ] Email notifications
- [ ] Responsive design improvements

### Phase 4
- [ ] User authentication improvements
- [ ] Multi-user support
- [ ] Collaboration features
- [ ] API endpoints

## Contributing

This is a personal project for managing university courses. Feel free to fork and adapt for your needs.

## License

MIT License - feel free to use and modify.

## Author

Created for managing Quantum Information Technology and Mathematical Modeling & Data Analysis programs at University of Gdańsk.

## Support

For questions or issues, please create an issue in the GitHub repository.
