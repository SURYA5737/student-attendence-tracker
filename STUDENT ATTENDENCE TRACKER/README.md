# STUDENT ATTENDENCE TRACKER

A simple and modern **Student Attendence Tracker** built with Python, Flask, SQLite, HTML and CSS.

> Note: The project title uses "ATTENDENCE" to match the requested project name. The correct spelling in normal English is "ATTENDANCE".

## Features

- Dashboard with live statistics
- Add and delete students
- Add and delete subjects
- Mark Present/Absent attendance
- Select attendance date and subject
- Update an existing attendance record for the same student/date/subject
- Automatic attendance percentage calculation
- Low attendance warning below 75%
- Responsive, modern UI
- SQLite database created automatically

## Technology

- Python 3
- Flask
- SQLite
- HTML5
- CSS3

## Run locally

### 1. Open the project in VS Code

### 2. Create a virtual environment (recommended)

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

### 5. Open in your browser

```text
http://127.0.0.1:5000
```

The `attendance.db` file is generated automatically after the first run.

## Project structure

```text
STUDENT ATTENDENCE TRACKER/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── students.html
│   ├── add_student.html
│   ├── subjects.html
│   ├── add_subject.html
│   ├── mark_attendance.html
│   └── report.html
└── static/
    └── style.css
```

## Database design

### Student
- id (Primary Key)
- name
- roll_no (Unique)
- department
- year

### Subject
- id (Primary Key)
- subject_name (Unique)

### Attendance
- id (Primary Key)
- student_id (Foreign Key)
- subject_id (Foreign Key)
- attendance_date
- status

## GitHub

Upload the source code and documentation files shown above. Do **not** upload:
- `attendance.db`
- `.venv/`
- `__pycache__/`
- personal secrets or passwords

These are already excluded by `.gitignore`.


## Recent fixes
- Roll numbers are sorted numerically (e.g. 83, 84, 100) instead of alphabetically.
- Student IDs restart from 1 after all students are deleted.
- The main dashboard title is **STUDENT ATTENDENCE TRACKER**.
