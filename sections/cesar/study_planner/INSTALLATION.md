# Study Planner - Installation Guide for Windows 11

Complete step-by-step installation guide for setting up Study Planner on Windows 11 with PyCharm.

## Prerequisites Check

You already have:
- ✅ Python 3.11.9 installed
- ✅ PyCharm downloading/installed

## Installation Steps

### Step 1: Download the Project

1. Download the entire `study_planner` folder
2. Save it to a location like: `C:\***\***\***\study_planner`

### Step 2: Open in PyCharm

1. Open PyCharm
2. Click **File → Open**
3. Navigate to your `study_planner` folder
4. Click **OK**

### Step 3: Create Virtual Environment

PyCharm will likely ask if you want to create a virtual environment. If it does:
1. Click **OK** to create a new virtual environment
2. Wait for it to finish

If it doesn't ask:
1. Go to **File → Settings** (or Ctrl+Alt+S)
2. Navigate to **Project: study_planner → Python Interpreter**
3. Click the gear icon ⚙️ → **Add**
4. Select **Virtualenv Environment**
5. Choose **New environment**
6. Base interpreter: Select Python 3.11
7. Click **OK**

### Step 4: Install Dependencies

Open PyCharm Terminal (View → Tool Windows → Terminal) and run:

```bash
pip install -r requirements.txt
```

Wait for all packages to install. This might take a few minutes.

### Step 5: Database Setup

In the PyCharm terminal, run these commands one by one:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

You should see output confirming the database tables were created.

### Step 6: Create Admin Account

Create a superuser account to access the admin panel:

```bash
python manage.py createsuperuser
```

You'll be asked to enter:
- Username: (choose any username, e.g., `admin`)
- Email: (can leave blank or enter your email)
- Password: (choose a strong password)
- Password confirmation: (repeat the password)

### Step 7: Run the Server

Start the development server:

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 8: Access the Application

Open your web browser and visit:

**Main Application**: http://127.0.0.1:8000/
**Admin Panel**: http://127.0.0.1:8000/admin/

Login with the username and password you created.

## Initial Setup in Admin Panel

After logging in to the admin panel, follow these steps:

### 1. Add Your Programs

1. Click on **Programs** → **Add Program**
2. Fill in the details:

**For Quantum Information Technology:**
- Name: `Quantum Information Technology`
- University: `University of Gdańsk`
- Faculty: `Faculty of Mathematics, Physics and Informatics`
- Degree type: `Master's Degree`
- Total ECTS required: `120`
- Is active: ✅ (checked)
- Color: `#3B82F6` (blue)

Click **Save**

**For Modelowanie Matematyczne:**
- Name: `Modelowanie Matematyczne i Analiza Danych`
- University: `University of Gdańsk`
- Faculty: `Faculty of Mathematics, Physics and Informatics`
- Degree type: `Master's Degree`
- Total ECTS required: `120`
- Is active: ✅ (checked)
- Color: `#10B981` (green)

Click **Save**

### 2. Add Courses

Click on **Courses** → **Add Course**

**Example for QIT:**
- Program: Select `Quantum Information Technology`
- Code: `QIT-101`
- Name: `Introduction to Quantum Mechanics`
- Semester: `Winter 2025/2026`
- Year: `1`
- Semester type: `Winter Semester`
- ECTS: `6`
- Course type: `Mandatory`
- Instructor: (name of your professor)
- Hours per week: `4`

Click **Save and add another** to add more courses.

Repeat for all your courses from both programs.

### 3. Enroll in Courses

Click on **Enrollments** → **Add Enrollment**
- User: Select your username
- Course: Select a course
- Status: `In Progress` (or `Planned`)
- Enrolled date: Select today's date
- Is passed: Leave unchecked (check only for completed courses)

Click **Save and add another** to add more enrollments.

### 4. Add Assignments (Optional)

Click on **Assignments** → **Add Assignment**
- Course: Select a course
- Title: e.g., `Homework 3 - Quantum Gates`
- Assignment type: `Homework`
- Due date: Select date and time
- Priority: `Medium` or `High`
- Max points: `100`

Click **Save**

## Accessing Different Views

After setting up your data:

1. **Dashboard**: http://127.0.0.1:8000/dashboard/
   - Overview of all programs
   - Upcoming deadlines
   - Current courses

2. **My Courses**: http://127.0.0.1:8000/courses/
   - List of all your enrolled courses
   - Filter by program, status, semester

3. **Assignments**: http://127.0.0.1:8000/assignments/
   - All assignments across courses
   - Filter by status (pending/completed/overdue)

4. **Statistics**: http://127.0.0.1:8000/statistics/
   - GPA calculations
   - Progress charts
   - Grade distribution

## Troubleshooting

### Problem: "No module named 'django'"
**Solution**: Make sure your virtual environment is activated and run:
```bash
pip install -r requirements.txt
```

### Problem: "Table doesn't exist"
**Solution**: Run migrations:
```bash
python manage.py migrate
```

### Problem: Can't access http://127.0.0.1:8000/
**Solution**: Make sure the server is running:
```bash
python manage.py runserver
```

### Problem: PyCharm can't find Python
**Solution**: 
1. File → Settings → Project → Python Interpreter
2. Make sure Python 3.11 is selected
3. Recreate virtual environment if needed

## Stopping the Server

To stop the development server:
- Press `Ctrl+C` in the terminal where the server is running

## Next Steps

You can now:
1. ✅ Add all your programs
2. ✅ Add all your courses
3. ✅ Enroll in courses
4. ✅ Track assignments and deadlines
5. ✅ Record grades
6. ✅ Monitor your progress



## Daily Usage

To start working:
1. Open PyCharm
2. Open Terminal
3. Run: `python manage.py runserver`
4. Open browser: http://127.0.0.1:8000/

When done:
- Press Ctrl+C in terminal to stop server
- Close PyCharm

Your data is saved in `db.sqlite3` and persists between sessions.
