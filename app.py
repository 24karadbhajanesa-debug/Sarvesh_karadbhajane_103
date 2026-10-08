from flask import Flask, request, jsonify, render_template
import sqlite3
import re
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("students.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            class_name TEXT NOT NULL,
            marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100),
            contact TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def valid_contact(contact):
    return bool(re.fullmatch(r"[0-9]{10}", contact))

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/students")
def get_students():
    search = request.args.get("search", "").strip()
    conn = get_db()
    if search:
        rows = conn.execute("""
            SELECT * FROM students
            WHERE name LIKE ? OR roll_no LIKE ? OR class_name LIKE ?
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()
    else:
        rows = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.post("/api/students")
def add_student():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    roll_no = str(data.get("roll_no", "")).strip()
    class_name = str(data.get("class_name", "")).strip()
    contact = str(data.get("contact", "")).strip()

    try:
        marks = float(data.get("marks"))
    except (TypeError, ValueError):
        return jsonify({"error": "Marks must be a number."}), 400

    if not all([name, roll_no, class_name, contact]):
        return jsonify({"error": "All fields are required."}), 400
    if not 0 <= marks <= 100:
        return jsonify({"error": "Marks must be between 0 and 100."}), 400
    if not valid_contact(contact):
        return jsonify({"error": "Contact must contain exactly 10 digits."}), 400

    conn = get_db()
    try:
        conn.execute("""
            INSERT INTO students (name, roll_no, class_name, marks, contact)
            VALUES (?, ?, ?, ?, ?)
        """, (name, roll_no, class_name, marks, contact))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Roll number already exists."}), 409
    conn.close()
    return jsonify({"message": "Student added successfully."}), 201

@app.put("/api/students/<int:student_id>")
def update_student(student_id):
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    roll_no = str(data.get("roll_no", "")).strip()
    class_name = str(data.get("class_name", "")).strip()
    contact = str(data.get("contact", "")).strip()

    try:
        marks = float(data.get("marks"))
    except (TypeError, ValueError):
        return jsonify({"error": "Marks must be a number."}), 400

    if not all([name, roll_no, class_name, contact]):
        return jsonify({"error": "All fields are required."}), 400
    if not 0 <= marks <= 100:
        return jsonify({"error": "Marks must be between 0 and 100."}), 400
    if not valid_contact(contact):
        return jsonify({"error": "Contact must contain exactly 10 digits."}), 400

    conn = get_db()
    try:
        cur = conn.execute("""
            UPDATE students
            SET name=?, roll_no=?, class_name=?, marks=?, contact=?
            WHERE id=?
        """, (name, roll_no, class_name, marks, contact, student_id))
        if cur.rowcount == 0:
            conn.close()
            return jsonify({"error": "Student not found."}), 404
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Roll number already exists."}), 409
    conn.close()
    return jsonify({"message": "Student updated successfully."})

@app.delete("/api/students/<int:student_id>")
def delete_student(student_id):
    conn = get_db()
    cur = conn.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({"error": "Student not found."}), 404
    return jsonify({"message": "Student deleted successfully."})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
