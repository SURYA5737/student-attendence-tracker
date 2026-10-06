# Useful SQL Queries

## View all students
```sql
SELECT * FROM students;
```

## View all subjects
```sql
SELECT * FROM subjects;
```

## View attendance
```sql
SELECT * FROM attendance;
```

## Count students
```sql
SELECT COUNT(*) FROM students;
```

## Count present records
```sql
SELECT COUNT(*) FROM attendance WHERE status = 'Present';
```

## Count absent records
```sql
SELECT COUNT(*) FROM attendance WHERE status = 'Absent';
```

## Attendance for one student
```sql
SELECT * FROM attendance WHERE student_id = 1;
```

## Attendance percentage
```sql
SELECT
    student_id,
    SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS percentage
FROM attendance
GROUP BY student_id;
```
