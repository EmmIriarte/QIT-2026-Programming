# Study Planner - Quick Start Guide

Quick reference for getting started and daily usage.

## 🚀 First Time Setup (5 minutes)

```bash
# 1. Open PyCharm with study_planner folder
# 2. Open Terminal in PyCharm
# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database
python manage.py migrate

# 5. Create admin account
python manage.py createsuperuser
# Enter username, email (optional), password

# 6. Start server
python manage.py runserver

# 7. Open browser
# Go to: http://127.0.0.1:8000/admin/
```

## 📚 Daily Usage

### Starting the Server
```bash
# Open PyCharm Terminal
python manage.py runserver
```

### Accessing the Application
- **Main App**: http://127.0.0.1:8000/
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### Stopping the Server
```
Press Ctrl+C in the terminal
```

## ⚡ Quick Tasks

### Add a New Program
1. Go to Admin Panel → Programs → Add Program
2. Fill in: Name, University, Degree Type, ECTS (120)
3. Choose a color for visual identification
4. Save

### Add a Course
1. Admin Panel → Courses → Add Course
2. Select Program
3. Fill in: Code, Name, Semester, ECTS
4. Save

### Enroll in a Course
1. Admin Panel → Enrollments → Add Enrollment
2. Select: Your user, Course
3. Set Status: "In Progress"
4. Save

### Add an Assignment
1. Admin Panel → Assignments → Add Assignment
2. Select Course
3. Fill in: Title, Due Date, Type, Max Points
4. Save

### Record a Grade
1. Admin Panel → Grades → Add Grade
2. Select: Enrollment, Assignment (optional)
3. Enter: Grade (2.0-5.0) or Points
4. Set Weight (for final grade calculation)
5. Save

## 📊 Understanding the Dashboard

### Top Cards
- **Total Courses**: All courses you've enrolled in
- **Overall GPA**: Average of all grades (Polish 5.0 scale)
- **Active Courses**: Courses marked "In Progress"

### Programs Progress
- Visual progress bars for each program
- Shows ECTS earned vs required
- Color-coded by program

### Upcoming Deadlines
- Next 7 days assignments
- Color-coded by urgency:
  - 🔴 Red: Due today
  - 🟡 Orange: Due tomorrow
  - 🔵 Blue: More than 2 days

### Current Courses
- All courses with status "In Progress"
- Shows current grades if available
- Click for detailed view

## 🎓 Common Workflows

### Planning a New Semester
1. Add all courses for the semester
2. Enroll yourself in each course
3. Add known assignments/exams with due dates
4. Set realistic goals

### During Semester
1. Check Dashboard daily for upcoming deadlines
2. Mark assignments as completed when done
3. Record grades as you receive them
4. Update notes on courses

### End of Semester
1. Mark all assignments as completed
2. Record final grades
3. Change enrollment status to "Completed"
4. Check "Is passed" if you passed the course

### Checking Progress
1. Go to Statistics page
2. View GPA per program
3. Check ECTS earned
4. See grade distribution

## 🔧 Useful Admin Panel Features

### Bulk Actions
- Select multiple items (checkboxes)
- Use dropdown for bulk actions
- Example: Mark multiple assignments as completed

### Filters
- Right sidebar has filters
- Filter by: Program, Status, Date, etc.
- Quick way to find specific items

### Search
- Search box at top right
- Search by: Course code, Title, Name
- Very fast for finding specific items

## 📱 Pages Overview

### Dashboard (`/dashboard/`)
- **Purpose**: Quick overview of everything
- **Use When**: Starting your day, checking what's due
- **Key Info**: GPA, upcoming deadlines, active courses

### My Courses (`/courses/`)
- **Purpose**: See all your enrolled courses
- **Use When**: Need to see all courses, filter by program/semester
- **Features**: Filter by program, status, semester type

### Assignments (`/assignments/`)
- **Purpose**: Manage all deadlines
- **Use When**: Planning your week, checking what's due
- **Features**: Filter by status (pending/completed/overdue)

### Statistics (`/statistics/`)
- **Purpose**: Track academic performance
- **Use When**: Want to see overall progress, GPA trends
- **Features**: Charts, grade distribution, ECTS progress

### Course Detail (`/course/<id>/`)
- **Purpose**: Deep dive into specific course
- **Use When**: Need all info about one course
- **Features**: All assignments, grades, notes for that course

## 💡 Pro Tips

### Tip 1: Use Colors
- Assign different colors to programs (QIT = Blue, MMAD = Green)
- Easy visual identification across the app

### Tip 2: Add Notes
- Use the Notes field in Enrollments
- Write tips, important dates, professor preferences
- Helps remember details about each course

### Tip 3: Prioritize Assignments
- Set priority (High/Medium/Low)
- Focus on high priority assignments first
- Use filters to see only high priority

### Tip 4: Regular Updates
- Update grades as soon as you get them
- Mark assignments done immediately
- Keeps your GPA calculation accurate

### Tip 5: Weekly Review
- Every Sunday, check upcoming week
- See what's due in next 7 days
- Plan your study schedule accordingly

## 🔍 Troubleshooting Quick Fixes

### Server won't start
```bash
# Check if another server is running
# Stop it with Ctrl+C
# Try again
python manage.py runserver
```

### Can't login
```bash
# Reset password
python manage.py changepassword yourusername
```

### Database issues
```bash
# Run migrations again
python manage.py migrate
```

### Missing data
- Check if you're logged in as correct user
- Check filters (might be hiding your data)
- Verify in admin panel


## 🎯 Best Practices

1. **Daily**: Check Dashboard for deadlines
2. **After Class**: Add any new assignments announced
3. **After Exam**: Record your grade
4. **Weekly**: Review progress, update course notes
5. **Monthly**: Check Statistics, verify GPA
6. **End of Semester**: Mark courses completed, update status

## 📊 Understanding GPA Calculation

Polish grading scale (2.0 - 5.0):
- **5.0**: Excellent (A)
- **4.5**: Very Good (B+)
- **4.0**: Good (B)
- **3.5**: Satisfactory Plus (C+)
- **3.0**: Satisfactory (C)
- **2.0**: Fail (F)

GPA is calculated as weighted average of all grades.

## 🆘 Need More Help?

- **Full Installation Guide**: See `INSTALLATION.md`
- **Sample Data**: See `SAMPLE_DATA.md`
- **Full Documentation**: See `README.md`

## ⌨️ Command Cheat Sheet

```bash
# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username

# Run tests
python manage.py test

# Collect static files (for production)
python manage.py collectstatic

# Open Python shell with Django
python manage.py shell
```

## 🎉 You're Ready!

Start by:
1. ✅ Adding your programs 
2. ✅ Adding this semester's courses
3. ✅ Enrolling in courses
4. ✅ Adding known deadlines
5. ✅ Checking dashboard daily

Happy studying! 📚🎓
