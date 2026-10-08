# Student Management System

Mini Web App Project — Aim 3

## Technology
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite
- Communication: REST API + JSON + Fetch API

## Features
- Add student
- View/list students
- Search by name, roll number, or class
- Update student details
- Delete student
- Duplicate roll-number validation
- Marks validation (0–100)
- 10-digit contact validation
- Dynamic updates without page reload
- Dashboard statistics

## How to Run

### 1. Open terminal in this folder
```bash
cd student_management_system
```

### 2. Create a virtual environment (recommended)
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Flask
```bash
pip install -r requirements.txt
```

### 4. Start the application
```bash
python app.py
```

### 5. Open in browser
Go to:
http://127.0.0.1:5000

The `students.db` SQLite database is created automatically on first run.
