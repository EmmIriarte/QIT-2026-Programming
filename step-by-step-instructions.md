# Step-by-Step Instructions: Running QIT-2026-Programming Project

This guide will walk you through setting up and running the Django project from scratch, even if you don't have anything installed on your computer.

## Prerequisites

You'll need:
- A computer (Mac, Windows, or Linux)
- Internet connection
- A terminal/command prompt

---

## Step 1: Install Python

Python is the programming language used for this project.

### For Mac:
1. Open Terminal (Applications → Utilities → Terminal)
2. Check if Python is already installed:
   ```bash
   python3 --version
   ```
3. If not installed, install Homebrew first (if you don't have it):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
4. Then install Python:
   ```bash
   brew install python3
   ```

### For Windows:
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or later
3. Run the installer
4. **Important:** Check the box "Add Python to PATH" during installation
5. Verify installation by opening Command Prompt (cmd) and typing:
   ```bash
   python --version
   ```

### For Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## Step 2: Install Conda (Recommended) or Use Python's venv

We'll use Conda to manage the project environment, but you can also use Python's built-in venv.

### Option A: Install Conda (Recommended)

#### For Mac:
1. Download Miniconda from: https://docs.conda.io/en/latest/miniconda.html
2. Choose the Mac installer (`.pkg` file)
3. Run the installer and follow the prompts
4. Restart Terminal
5. Verify installation:
   ```bash
   conda --version
   ```

#### For Windows:
1. Download Miniconda from: https://docs.conda.io/en/latest/miniconda.html
2. Choose the Windows installer (`.exe` file)
3. Run the installer and follow the prompts
4. Check "Add Miniconda to PATH" during installation
5. Restart Command Prompt
6. Verify installation:
   ```bash
   conda --version
   ```

#### For Linux:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Follow the prompts, then restart terminal
```

### Option B: Use Python's venv (Alternative)

If you don't want to install Conda, you can use Python's built-in virtual environment:

#### For Mac/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### For Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## Step 3: Get the Project Files

### Option A: Clone from GitHub (if you have git installed)
```bash
git clone https://github.com/EmmIriarte/QIT-2026-Programming.git
cd QIT-2026-Programming
```

### Option B: Download from GitHub
1. Go to: https://github.com/EmmIriarte/QIT-2026-Programming
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file
5. Open Terminal/Command Prompt and navigate to the extracted folder:
   ```bash
   cd path/to/QIT-2026-Programming
   ```

---

## Step 4: Create Conda Environment (If using Conda)

1. Open Terminal/Command Prompt
2. Navigate to the project directory:
   ```bash
   cd path/to/QIT-2026-Programming
   ```
   (Replace `path/to/` with the actual path to your project folder)

3. Create a new Conda environment with Python 3.11:
   ```bash
   conda create -n qit-2026-django python=3.11 -y
   ```

4. Activate the environment:
   ```bash
   conda activate qit-2026-django
   ```

   **Note:** You'll see `(qit-2026-django)` in your terminal prompt when the environment is active.

---

## Step 5: Install Django

With your environment activated, install Django:

### If using Conda:
```bash
pip install Django>=4.2
```

### If using venv (Option B from Step 2):
```bash
pip install -r requirements.txt
```

This will install Django and all other required packages.

**Verify Django installation:**
```bash
python -m django --version
```

You should see something like: `Django 5.2.10` or similar.

---

## Step 6: Navigate to Project Directory

Make sure you're in the project root directory:

```bash
cd /path/to/QIT-2026-Programming
```

**On Mac/Linux:** Use the full path like `/Users/yourname/Desktop/QIT-2026-Programming`

**On Windows:** Use the full path like `C:\Users\yourname\Desktop\QIT-2026-Programming`

---

## Step 7: Run the Django Development Server

1. Make sure your Conda environment is activated (you should see `(qit-2026-django)` in your prompt)

2. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

3. You should see output like:
   ```
   Watching for file changes with StatReloader
   Performing system checks...

   System check identified no issues (0 silenced).

   You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
   Run 'python manage.py migrate' to apply them.
   Django version 5.2.10, using settings 'core.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```

   **Note:** The migration warning is normal and can be ignored - this project doesn't use a database.

4. The server is now running! 🎉

---

## Step 8: Access the Application

1. Open your web browser (Chrome, Firefox, Safari, etc.)

2. Go to: **http://127.0.0.1:8000/** or **http://localhost:8000/**

3. You should see the **Global Index** page listing all students:
   - Juan Pablo
   - Cesar
   - Atheer
   - Emmanuel Aram Iriarte Olea
   - Praneet
   - Frankie

4. Click on any student's name to see their section

5. For example, click "Emmanuel Aram Iriarte Olea" to see:
   - Application 1: LeetCode Problem (Longest Palindromic Substring)
   - Application 2: Basic Quantum Gates Simulator
   - Application 3: Dynamic Programming Example

---

## Step 9: Stop the Server

When you're done testing:

1. Go back to your Terminal/Command Prompt
2. Press `Ctrl + C` (or `Cmd + C` on Mac) to stop the server
3. Deactivate the Conda environment (optional):
   ```bash
   conda deactivate
   ```

---

## Troubleshooting

### Problem: "python: command not found" or "python3: command not found"
**Solution:** Python is not installed or not in PATH. Reinstall Python and make sure to check "Add Python to PATH" (Windows).

### Problem: "conda: command not found"
**Solution:** 
- Restart your terminal after installing Conda
- On Mac/Linux, you may need to run: `source ~/.bashrc` or `source ~/.zshrc`
- On Windows, make sure Conda was added to PATH during installation

### Problem: "ModuleNotFoundError: No module named 'django'"
**Solution:** Make sure your Conda environment is activated (`conda activate qit-2026-django`) and Django is installed (`pip install Django>=4.2`).

### Problem: "Error: That port is already in use"
**Solution:** Another process is using port 8000. Either:
- Stop the other process
- Run Django on a different port: `python manage.py runserver 8001`

### Problem: "ImportError" or other Python errors
**Solution:** Make sure you're in the correct directory (project root) and your environment is activated.

### Problem: Can't access http://127.0.0.1:8000/
**Solution:**
- Make sure the server is running (you should see the "Starting development server" message)
- Try `http://localhost:8000/` instead
- Check your firewall settings

---

## Quick Reference

### Start the server (every time you want to run the project):

```bash
# 1. Navigate to project directory
cd /path/to/QIT-2026-Programming

# 2. Activate Conda environment
conda activate qit-2026-django

# 3. Run the server
python manage.py runserver

# 4. Open browser to http://127.0.0.1:8000/
```

### Stop the server:
- Press `Ctrl + C` (or `Cmd + C` on Mac) in the terminal

### Common URLs:
- Global Index: `http://127.0.0.1:8000/`
- Emmanuel's Section: `http://127.0.0.1:8000/emmanuel_aram_iriarte_olea/`
- Emmanuel's App 1: `http://127.0.0.1:8000/emmanuel_aram_iriarte_olea/app1/`
- Emmanuel's App 2: `http://127.0.0.1:8000/emmanuel_aram_iriarte_olea/app2/`
- Emmanuel's App 3: `http://127.0.0.1:8000/emmanuel_aram_iriarte_olea/app3/`

---

## Additional Notes

- **First time setup:** Steps 1-5 only need to be done once on your computer
- **Every time you work on the project:** Steps 6-7 (navigate to project, activate environment, run server)
- **The migration warning is normal:** This project doesn't use a database, so you can ignore the migration warnings
- **Virtual environments:** Always activate your Conda environment before working on the project

---

## Need Help?

If you encounter any issues not covered here:
1. Check that all prerequisites are installed correctly
2. Make sure your Conda environment is activated
3. Verify you're in the correct project directory
4. Check the error messages in your terminal for specific guidance

Happy coding! 🚀
