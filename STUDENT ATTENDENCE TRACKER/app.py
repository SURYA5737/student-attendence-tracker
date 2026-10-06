from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import date
from pathlib import Path

app = Flask(__name__)
app.secret_key = "student-attendance-tracker-secret"
DATABASE = Path(__file__).with_name("attendance.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            year TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY,
            subject_name TEXT NOT NULL UNIQUE
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Present','Absent')),
            UNIQUE(student_id, subject_id, attendance_date),
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    student_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    subject_count = conn.execute("SELECT COUNT(*) FROM subjects").fetchone()[0]
    attendance_count = conn.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
    present_count = conn.execute(
        "SELECT COUNT(*) FROM attendance WHERE status='Present'"
    ).fetchone()[0]
    absent_count = attendance_count - present_count
    conn.close()
    return render_template(
        "index.html",
        student_count=student_count,
        subject_count=subject_count,
        attendance_count=attendance_count,
        present_count=present_count,
        absent_count=absent_count,
    )


@app.route("/students")
def students():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY CAST(roll_no AS INTEGER), roll_no").fetchall()
    conn.close()
    return render_template("students.html", students=students)


@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"].strip()
        roll_no = request.form["roll_no"].strip()
        department = request.form["department"].strip()
        year = request.form["year"].strip()

        if not all([name, roll_no, department, year]):
            flash("Please fill all student details.", "error")
            return render_template("add_student.html")

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO students (name, roll_no, department, year) VALUES (?, ?, ?, ?)",
                (name, roll_no, department, year),
            )
            conn.commit()
            flash("Student added successfully.", "success")
        except sqlite3.IntegrityError:
            flash("That roll number already exists.", "error")
        finally:
            conn.close()
        return redirect(url_for("students"))

    return render_template("add_student.html")


@app.route("/delete_student/<int:id>")
def delete_student(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    # If the student list becomes empty, reset SQLite's AUTOINCREMENT
    # sequence from older database versions so the next student starts at ID 1.
    remaining = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if remaining == 0:
        try:
            conn.execute("DELETE FROM sqlite_sequence WHERE name='students'")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()
    flash("Student deleted.", "success")
    return redirect(url_for("students"))


@app.route("/subjects")
def subjects():
    conn = get_db()
    subjects = conn.execute("SELECT * FROM subjects ORDER BY subject_name").fetchall()
    conn.close()
    return render_template("subjects.html", subjects=subjects)


@app.route("/add_subject", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        subject_name = request.form["subject_name"].strip()
        if not subject_name:
            flash("Enter a subject name.", "error")
            return render_template("add_subject.html")

        conn = get_db()
        try:
            conn.execute("INSERT INTO subjects (subject_name) VALUES (?)", (subject_name,))
            conn.commit()
            flash("Subject added successfully.", "success")
        except sqlite3.IntegrityError:
            flash("That subject already exists.", "error")
        finally:
            conn.close()
        return redirect(url_for("subjects"))

    return render_template("add_subject.html")


@app.route("/delete_subject/<int:id>")
def delete_subject(id):
    conn = get_db()
    conn.execute("DELETE FROM subjects WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Subject deleted.", "success")
    return redirect(url_for("subjects"))


@app.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY CAST(roll_no AS INTEGER), roll_no").fetchall()
    subjects = conn.execute("SELECT * FROM subjects ORDER BY subject_name").fetchall()

    if request.method == "POST":
        subject_id = request.form["subject_id"]
        attendance_date = request.form["attendance_date"]

        for student in students:
            status = request.form.get(f"status_{student['id']}")
            if status:
                conn.execute(
                    """
                    INSERT INTO attendance
                    (student_id, subject_id, attendance_date, status)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(student_id, subject_id, attendance_date)
                    DO UPDATE SET status=excluded.status
                    """,
                    (student["id"], subject_id, attendance_date, status),
                )

        conn.commit()
        conn.close()
        flash("Attendance saved successfully.", "success")
        return redirect(url_for("report"))

    conn.close()
    return render_template(
        "mark_attendance.html",
        students=students,
        subjects=subjects,
        today=date.today().isoformat(),
    )


@app.route("/report")
def report():
    conn = get_db()
    students = conn.execute("SELECT * FROM students ORDER BY CAST(roll_no AS INTEGER), roll_no").fetchall()
    report_data = []

    for student in students:
        total = conn.execute(
            "SELECT COUNT(*) FROM attendance WHERE student_id=?",
            (student["id"],),
        ).fetchone()[0]
        present = conn.execute(
            "SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'",
            (student["id"],),
        ).fetchone()[0]
        percentage = round((present / total) * 100, 2) if total else 0

        report_data.append({
            "id": student["id"],
            "name": student["name"],
            "roll_no": student["roll_no"],
            "department": student["department"],
            "year": student["year"],
            "total": total,
            "present": present,
            "absent": total - present,
            "percentage": percentage,
        })

    conn.close()
    return render_template("report.html", report=report_data)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
