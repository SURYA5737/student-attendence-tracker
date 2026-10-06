# Student Attendance Management System

## 1. Introduction
The Student Attendance Management System is a simple DBMS-based web application developed to record and monitor student attendance efficiently.

## 2. Objective
- Maintain student records.
- Maintain subject records.
- Record daily attendance.
- Calculate attendance percentage automatically.
- Identify students with attendance below 75%.

## 3. Modules
1. Dashboard
2. Student Management
3. Subject Management
4. Attendance Management
5. Attendance Report

## 4. Technologies
- Python
- Flask
- SQLite
- HTML
- CSS

## 5. Database Tables
### Student
Stores student identity and academic information.

### Subject
Stores subjects.

### Attendance
Stores student attendance by subject and date.

## 6. Working
The user first creates student and subject records. Attendance is then marked for a selected subject and date. Records are stored in SQLite. The report page counts total and present records and calculates the attendance percentage.

## 7. Formula
Attendance Percentage = (Present Classes / Total Classes) × 100

## 8. Conclusion
The system provides a simple and efficient way to manage student attendance and generate attendance reports using a relational database.
